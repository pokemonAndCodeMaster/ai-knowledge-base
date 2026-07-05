"""Data access for manual-QC read models."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from psycopg2.extras import Json

from src.api.schemas.acceptance import QuerySpec
from src.database import PostgresConnector


class AcceptanceRepository:
    _FILTER_FIELDS = {"name": "task.dataset_name", "topic": "task.topic", "priority": "task.priority", "status": "task.status"}
    _SORT_FIELDS = {**_FILTER_FIELDS, "expected_delivery_at": "task.expected_delivery_at", "annotation_submitted": "annotation_submitted"}

    def __init__(self, postgres: PostgresConnector) -> None:
        self._postgres = postgres

    def query_tasks(self, spec: QuerySpec) -> tuple[list[dict[str, Any]], int]:
        where_sql, params = self._build_filters(spec)
        order_sql = self._build_sort(spec)
        items = self._postgres.fetch_all(
            f"""
            SELECT task.id, task.task_code, task.dataset_name AS name, task.scene_name,
                   task.topic, task.priority, task.status, task.expected_delivery_at,
                   task.expected_quantity,
                   COALESCE(SUM(s.annotation_total), 0)::INT AS annotation_total,
                   COALESCE(SUM(s.annotation_submitted), 0)::INT AS annotation_submitted,
                   COALESCE(SUM(s.annotation_pending), 0)::INT AS annotation_pending,
                   COALESCE(SUM(s.acceptance_allocated), 0)::INT AS acceptance_allocated,
                   COALESCE(SUM(s.acceptance_submitted), 0)::INT AS acceptance_submitted,
                   COALESCE(SUM(s.good_allocated), 0)::INT AS good_allocated,
                   COALESCE(SUM(s.good_passed), 0)::INT AS good_passed,
                   COALESCE(SUM(s.bad_allocated), 0)::INT AS bad_allocated,
                   COALESCE(SUM(s.bad_passed), 0)::INT AS bad_passed,
                   COALESCE((SELECT jsonb_agg(jsonb_build_object('stat_date', recent.stat_date, 'submitted', recent.submitted) ORDER BY recent.stat_date DESC)
                             FROM (SELECT stat_date, SUM(annotation_submitted)::INT AS submitted
                                   FROM t_qc_daily_snapshot
                                   WHERE scene_name = task.scene_name AND annotation_submitted > 0
                                   GROUP BY stat_date ORDER BY stat_date DESC LIMIT 4) recent), '[]'::jsonb) AS recent_annotation_days
            FROM t_qc_delivery_task task
            LEFT JOIN t_qc_daily_snapshot s ON s.scene_name = task.scene_name
            {where_sql}
            GROUP BY task.id
            {order_sql}
            LIMIT %s OFFSET %s
            """,
            [*params, spec.page_size, (spec.page - 1) * spec.page_size],
        )
        total_row = self._postgres.fetch_one(f"SELECT COUNT(*)::INT AS total FROM t_qc_delivery_task task {where_sql}", params)
        return items, int(total_row["total"] if total_row else 0)

    def get_daily_breakdown(self, task_id: int) -> list[dict[str, Any]] | None:
        task = self._postgres.fetch_one("SELECT scene_name FROM t_qc_delivery_task WHERE id = %s", [task_id])
        if task is None:
            return None
        return self._postgres.fetch_all(
            """
            SELECT CONCAT(%s, '-date-', TO_CHAR(stat_date, 'YYYY-MM-DD')) AS id, stat_date,
                   SUM(annotation_total)::INT AS annotation_total,
                   SUM(annotation_submitted)::INT AS annotation_submitted,
                   SUM(annotation_pending)::INT AS annotation_pending,
                   SUM(acceptance_allocated)::INT AS acceptance_allocated,
                   SUM(acceptance_submitted)::INT AS acceptance_submitted,
                   SUM(good_allocated)::INT AS good_allocated,
                   SUM(good_passed)::INT AS good_passed,
                   SUM(bad_allocated)::INT AS bad_allocated,
                   SUM(bad_passed)::INT AS bad_passed
            FROM t_qc_daily_snapshot WHERE scene_name = %s
            GROUP BY stat_date ORDER BY stat_date DESC
            """,
            [task_id, task["scene_name"]],
        )

    def resolve_filtered_task_ids(self, spec: QuerySpec) -> list[int]:
        where_sql, params = self._build_filters(spec)
        rows = self._postgres.fetch_all(
            f"SELECT task.id FROM t_qc_delivery_task task {where_sql} ORDER BY task.id LIMIT 5000",
            params,
        )
        return [int(row["id"]) for row in rows]

    def get_selection_units(
        self,
        task_ids: Sequence[int],
        date_keys: Sequence[tuple[int, str]],
    ) -> list[dict[str, Any]]:
        if not task_ids and not date_keys:
            return []
        clauses: list[str] = []
        params: list[Any] = []
        if task_ids:
            clauses.append("task.id = ANY(%s)")
            params.append(list(task_ids))
        if date_keys:
            date_clauses: list[str] = []
            for task_id, stat_date in date_keys:
                date_clauses.append("(task.id = %s AND snapshot.stat_date = %s)")
                params.extend([task_id, stat_date])
            clauses.append("(" + " OR ".join(date_clauses) + ")")
        return self._postgres.fetch_all(
            f"""
            SELECT id, task_id, task_name, topic, scene_name, stat_date, available,
                   LEAST(good_raw_available, available)::INT AS good_available,
                   GREATEST(available - LEAST(good_raw_available, available), 0)::INT AS bad_available,
                   computed_at
            FROM (
                SELECT CONCAT(task.id, '-date-', TO_CHAR(snapshot.stat_date, 'YYYY-MM-DD')) AS id,
                       task.id AS task_id, task.dataset_name AS task_name, task.topic,
                       task.scene_name, task.priority, task.expected_delivery_at, snapshot.stat_date,
                       GREATEST(SUM(snapshot.annotation_submitted - snapshot.acceptance_allocated), 0)::INT AS available,
                       GREATEST(SUM(COALESCE((snapshot.option_annotation->>'GOOD')::INT, 0) - snapshot.good_allocated), 0)::INT AS good_raw_available,
                       MAX(snapshot.computed_at) AS computed_at
                FROM t_qc_delivery_task task
                JOIN t_qc_daily_snapshot snapshot ON snapshot.scene_name = task.scene_name
                WHERE ({' OR '.join(clauses)}) AND snapshot.annotation_submitted > snapshot.acceptance_allocated
                GROUP BY task.id, task.dataset_name, task.topic, task.scene_name,
                         task.priority, task.expected_delivery_at, snapshot.stat_date
            ) units
            ORDER BY priority, expected_delivery_at NULLS LAST, task_id, stat_date DESC
            """,
            params,
        )

    def save_preview(
        self,
        *,
        preview_id: str,
        created_by: str,
        selection_spec: dict[str, Any],
        request_payload: dict[str, Any],
        result_summary: dict[str, Any],
        source_version: str,
        expires_at: datetime,
    ) -> None:
        self._postgres.execute(
            """
            INSERT INTO t_qc_operation_preview
                (preview_id, operation_type, created_by, selection_spec, request_payload,
                 result_summary, source_version, status, expires_at)
            VALUES (%s, 'ACCEPTANCE_ASSIGNMENT', %s, %s, %s, %s, %s, 'READY', %s)
            """,
            [
                preview_id,
                created_by,
                Json(selection_spec),
                Json(request_payload),
                Json(result_summary),
                source_version,
                expires_at,
            ],
        )

    def get_preview(self, preview_id: str, created_by: str) -> dict[str, Any] | None:
        return self._postgres.fetch_one(
            """
            SELECT result_summary, status, expires_at
            FROM t_qc_operation_preview
            WHERE preview_id = %s AND created_by = %s
            """,
            [preview_id, created_by],
        )

    def _build_filters(self, spec: QuerySpec) -> tuple[str, list[Any]]:
        clauses: list[str] = []
        params: list[Any] = []
        for item in spec.filters:
            column = self._FILTER_FIELDS[item.field]
            if item.operator == "contains":
                clauses.append(f"{column} ILIKE %s")
                params.append(f"%{item.value}%")
            elif item.operator == "in":
                values = list(item.value)
                if values:
                    clauses.append(f"{column} = ANY(%s)")
                    params.append(values)
            else:
                clauses.append(f"{column} = %s")
                params.append(item.value)
        return ("WHERE " + " AND ".join(clauses), params) if clauses else ("", params)

    def _build_sort(self, spec: QuerySpec) -> str:
        if not spec.sorting:
            return "ORDER BY task.priority ASC, task.expected_delivery_at ASC NULLS LAST, task.id ASC"
        return "ORDER BY " + ", ".join(f"{self._SORT_FIELDS[item.field]} {item.direction.upper()}" for item in spec.sorting)
