"""FastAPI routes for the acceptance first vertical slice."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Query

from src.api.deps import get_acceptance_query_service, get_assignment_preview_service
from src.api.schemas.acceptance import (
    AcceptanceDailyItem,
    AcceptanceTaskPage,
    AssignmentPreviewRequest,
    AssignmentPreviewResponse,
    QuerySpec,
)
from src.api.schemas.common import ApiResponse
from src.manual_qc.acceptance.services.assignment_preview_service import AssignmentPreviewService, InvalidSelectionError
from src.manual_qc.acceptance.services.query_service import AcceptanceQueryService


router = APIRouter(prefix="/api/v1/manual-qc/acceptance", tags=["manual-qc-acceptance"])


@router.post("/tasks/query", response_model=ApiResponse[AcceptanceTaskPage])
def query_tasks(spec: QuerySpec, service: AcceptanceQueryService = Depends(get_acceptance_query_service)) -> ApiResponse[AcceptanceTaskPage]:
    return ApiResponse(data=service.query_tasks(spec))


@router.get("/tasks/{task_id}/breakdown", response_model=ApiResponse[list[AcceptanceDailyItem]])
def get_breakdown(task_id: int, dimension: str = Query(default="date"), service: AcceptanceQueryService = Depends(get_acceptance_query_service)) -> ApiResponse[list[AcceptanceDailyItem]]:
    if dimension != "date":
        raise HTTPException(status_code=400, detail={"code": "DIMENSION_NOT_IMPLEMENTED", "dimension": dimension})
    rows = service.get_daily_breakdown(task_id)
    if rows is None:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND", "task_id": task_id})
    return ApiResponse(data=rows)


@router.get("/metadata", response_model=ApiResponse[dict[str, object]])
def metadata() -> ApiResponse[dict[str, object]]:
    return ApiResponse(data={"expand_dimensions": [{"value": "date", "label": "按天", "implemented": True}, {"value": "group", "label": "按标注组", "implemented": False}, {"value": "annotator", "label": "按标注员", "implemented": False}, {"value": "scene", "label": "按专题", "implemented": False}], "page_sizes": [20, 50, 100, 200], "samplers": [{"value": "ratio", "label": "按 Good/Bad 比例"}]})


@router.post("/assignment/preview", response_model=ApiResponse[AssignmentPreviewResponse])
def create_assignment_preview(
    request: AssignmentPreviewRequest,
    service: AssignmentPreviewService = Depends(get_assignment_preview_service),
    employee_id: str = Header(default="local-reviewer", alias="X-Employee-Id"),
) -> ApiResponse[AssignmentPreviewResponse]:
    try:
        preview = service.create_preview(request, employee_id)
    except InvalidSelectionError as exc:
        raise HTTPException(status_code=422, detail={"code": "INVALID_SELECTION", "message": str(exc)}) from exc
    return ApiResponse(data=preview)


@router.get("/assignment/previews/{preview_id}", response_model=ApiResponse[AssignmentPreviewResponse])
def get_assignment_preview(
    preview_id: str,
    service: AssignmentPreviewService = Depends(get_assignment_preview_service),
    employee_id: str = Header(default="local-reviewer", alias="X-Employee-Id"),
) -> ApiResponse[AssignmentPreviewResponse]:
    preview = service.get_preview(preview_id, employee_id)
    if preview is None:
        raise HTTPException(status_code=404, detail={"code": "PREVIEW_NOT_FOUND_OR_EXPIRED"})
    return ApiResponse(data=preview)
