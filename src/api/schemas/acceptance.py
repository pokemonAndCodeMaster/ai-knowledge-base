"""HTTP contracts for the first manual-QC acceptance vertical slice."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class FilterSpec(BaseModel):
    field: Literal["name", "topic", "priority", "status"]
    operator: Literal["contains", "eq", "in"] = "eq"
    value: Any


class SortSpec(BaseModel):
    field: Literal["name", "topic", "priority", "status", "expected_delivery_at", "annotation_submitted"]
    direction: Literal["asc", "desc"] = "asc"


class QuerySpec(BaseModel):
    filters: list[FilterSpec] = Field(default_factory=list)
    sorting: list[SortSpec] = Field(default_factory=list)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)


class SelectionSpec(BaseModel):
    mode: Literal["explicit", "filtered"] = "explicit"
    explicit_ids: list[str] = Field(default_factory=list, max_items=5000)
    filter_snapshot: QuerySpec | None = None
    excluded_ids: list[str] = Field(default_factory=list, max_items=5000)
    leaf_dimension: Literal["task", "date", "group", "annotator", "scene"] = "date"


class AssignmentRuleSpec(BaseModel):
    strategy: Literal["ratio"] = "ratio"
    target_count: int | None = Field(default=None, ge=1)
    good_ratio: float = Field(default=0.5, ge=0, le=1)


class AssignmentPreviewRequest(BaseModel):
    selection: SelectionSpec
    rule: AssignmentRuleSpec = Field(default_factory=AssignmentRuleSpec)


class AssignmentPreviewItem(BaseModel):
    id: str
    task_id: int
    task_name: str
    topic: str
    scene_name: str
    stat_date: date
    available: int
    good_available: int
    bad_available: int
    planned_good: int
    planned_bad: int


class AssignmentPreviewResponse(BaseModel):
    preview_id: str
    status: Literal["READY"] = "READY"
    expires_at: datetime
    source_version: str
    selected_units: int
    total_available: int
    target_count: int
    planned_good: int
    planned_bad: int
    shortage: int
    items: list[AssignmentPreviewItem]
    warnings: list[str] = Field(default_factory=list)


class RecentAnnotationDay(BaseModel):
    stat_date: date
    submitted: int


class AcceptanceTaskItem(BaseModel):
    id: int
    task_code: str
    name: str
    scene_name: str
    topic: str
    priority: str
    status: str
    expected_delivery_at: date | None
    expected_quantity: int
    annotation_total: int
    annotation_submitted: int
    annotation_pending: int
    acceptance_allocated: int
    acceptance_submitted: int
    good_allocated: int
    good_passed: int
    bad_allocated: int
    bad_passed: int
    recent_annotation_days: list[RecentAnnotationDay] = Field(default_factory=list)


class AcceptanceTaskPage(BaseModel):
    items: list[AcceptanceTaskItem]
    total: int
    page: int
    page_size: int
    computed_at: datetime


class AcceptanceDailyItem(BaseModel):
    id: str
    stat_date: date
    annotation_total: int
    annotation_submitted: int
    annotation_pending: int
    acceptance_allocated: int
    acceptance_submitted: int
    good_allocated: int
    good_passed: int
    bad_allocated: int
    bad_passed: int
