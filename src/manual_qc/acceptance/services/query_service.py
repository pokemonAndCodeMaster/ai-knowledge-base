"""Read-only acceptance queue application service."""

from __future__ import annotations

from datetime import datetime, timezone

from src.api.schemas.acceptance import AcceptanceTaskPage, QuerySpec
from src.manual_qc.repository import AcceptanceRepository


class AcceptanceQueryService:
    def __init__(self, repository: AcceptanceRepository) -> None:
        self._repository = repository

    def query_tasks(self, spec: QuerySpec) -> AcceptanceTaskPage:
        items, total = self._repository.query_tasks(spec)
        return AcceptanceTaskPage(items=items, total=total, page=spec.page, page_size=spec.page_size, computed_at=datetime.now(timezone.utc))

    def get_daily_breakdown(self, task_id: int) -> list[dict[str, object]] | None:
        return self._repository.get_daily_breakdown(task_id)
