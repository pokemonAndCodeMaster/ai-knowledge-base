"""Resolve a selection, calculate a quota preview, and freeze it in PostgreSQL."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.api.schemas.acceptance import (
    AssignmentPreviewItem,
    AssignmentPreviewRequest,
    AssignmentPreviewResponse,
    SelectionSpec,
)
from src.manual_qc.acceptance.sampler import SamplingBucket, plan_ratio_sampling
from src.manual_qc.repository import AcceptanceRepository


_DATE_ID = re.compile(r"^(?P<task_id>\d+)-date-(?P<stat_date>\d{4}-\d{2}-\d{2})$")


class InvalidSelectionError(ValueError):
    pass


class AssignmentPreviewService:
    def __init__(self, repository: AcceptanceRepository, ttl_minutes: int = 30) -> None:
        self._repository = repository
        self._ttl = timedelta(minutes=ttl_minutes)

    def create_preview(
        self,
        request: AssignmentPreviewRequest,
        actor_id: str,
    ) -> AssignmentPreviewResponse:
        task_ids, date_keys = self._resolve_selection(request.selection)
        rows = self._repository.get_selection_units(task_ids, date_keys)
        excluded = set(request.selection.excluded_ids)
        rows = [row for row in rows if str(row["id"]) not in excluded and str(row["task_id"]) not in excluded]
        if not rows:
            raise InvalidSelectionError("当前选择没有可用于验收分配的已提交数据")

        buckets = [
            SamplingBucket(
                id=str(row["id"]),
                good_available=int(row["good_available"]),
                bad_available=int(row["bad_available"]),
            )
            for row in rows
        ]
        plan = plan_ratio_sampling(buckets, request.rule.target_count, request.rule.good_ratio)
        items = [
            AssignmentPreviewItem(
                id=str(row["id"]),
                task_id=int(row["task_id"]),
                task_name=str(row["task_name"]),
                topic=str(row["topic"]),
                scene_name=str(row["scene_name"]),
                stat_date=row["stat_date"],
                available=int(row["available"]),
                good_available=int(row["good_available"]),
                bad_available=int(row["bad_available"]),
                planned_good=plan.allocations[str(row["id"])][0],
                planned_bad=plan.allocations[str(row["id"])][1],
            )
            for row in rows
        ]
        source_version = self._source_version(rows)
        now = datetime.now(timezone.utc)
        response = AssignmentPreviewResponse(
            preview_id=f"ap_{uuid4().hex}",
            expires_at=now + self._ttl,
            source_version=source_version,
            selected_units=len(items),
            total_available=sum(item.available for item in items),
            target_count=plan.target_count,
            planned_good=plan.planned_good,
            planned_bad=plan.planned_bad,
            shortage=plan.shortage,
            items=items,
            warnings=list(plan.warnings),
        )
        selection_payload = request.selection.model_dump(mode="json")
        request_payload = request.model_dump(mode="json")
        result_payload = response.model_dump(mode="json")
        self._repository.save_preview(
            preview_id=response.preview_id,
            created_by=actor_id,
            selection_spec=selection_payload,
            request_payload=request_payload,
            result_summary=result_payload,
            source_version=source_version,
            expires_at=response.expires_at,
        )
        return response

    def get_preview(self, preview_id: str, actor_id: str) -> AssignmentPreviewResponse | None:
        row = self._repository.get_preview(preview_id, actor_id)
        if row is None or row["status"] != "READY" or row["expires_at"] <= datetime.now(timezone.utc):
            return None
        return AssignmentPreviewResponse.parse_obj(row["result_summary"])

    def _resolve_selection(self, selection: SelectionSpec) -> tuple[list[int], list[tuple[int, str]]]:
        if selection.leaf_dimension not in {"task", "date"}:
            raise InvalidSelectionError(f"当前版本尚未支持 {selection.leaf_dimension} 叶子维度")
        if selection.mode == "filtered":
            if selection.filter_snapshot is None:
                raise InvalidSelectionError("筛选全选必须携带 filter_snapshot")
            return self._repository.resolve_filtered_task_ids(selection.filter_snapshot), []
        if not selection.explicit_ids:
            raise InvalidSelectionError("请至少选择一个任务或日期")

        task_ids: list[int] = []
        date_keys: list[tuple[int, str]] = []
        for item_id in selection.explicit_ids:
            if item_id.isdigit():
                task_ids.append(int(item_id))
                continue
            match = _DATE_ID.fullmatch(item_id)
            if match is None:
                raise InvalidSelectionError(f"无法识别选择项：{item_id}")
            date_keys.append((int(match.group("task_id")), match.group("stat_date")))
        return sorted(set(task_ids)), sorted(set(date_keys))

    @staticmethod
    def _source_version(rows: list[dict[str, object]]) -> str:
        payload = [
            [str(row["id"]), int(row["available"]), str(row["computed_at"])]
            for row in rows
        ]
        return "sha256:" + hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:24]
