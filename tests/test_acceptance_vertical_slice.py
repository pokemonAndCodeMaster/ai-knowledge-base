import unittest
from datetime import date, datetime, timezone

from src.api.app import create_app
from src.api.schemas.acceptance import (
    AcceptanceDailyItem,
    AssignmentPreviewRequest,
    AssignmentRuleSpec,
    FilterSpec,
    QuerySpec,
    SelectionSpec,
    SortSpec,
)
from src.manual_qc.acceptance.sampler import SamplingBucket, plan_ratio_sampling
from src.manual_qc.acceptance.services.assignment_preview_service import AssignmentPreviewService, InvalidSelectionError
from src.manual_qc.acceptance.router import get_breakdown, metadata, query_tasks
from src.manual_qc.acceptance.services.query_service import AcceptanceQueryService
from src.manual_qc.repository import AcceptanceRepository


class FakePostgres:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def fetch_all(self, sql: str, params: object = None):
        self.calls.append((sql, params))
        return [
            {
                "id": 1,
                "task_code": "E2E-001",
                "name": "城区测试任务",
                "scene_name": "E2E_CITY",
                "topic": "城区",
                "priority": "P0",
                "status": "ACCEPTANCE_RUNNING",
                "expected_delivery_at": None,
                "expected_quantity": 100,
                "annotation_total": 100,
                "annotation_submitted": 80,
                "annotation_pending": 20,
                "acceptance_allocated": 20,
                "acceptance_submitted": 10,
                "good_allocated": 16,
                "good_passed": 15,
                "bad_allocated": 4,
                "bad_passed": 2,
                "recent_annotation_days": [],
            }
        ]

    def fetch_one(self, sql: str, params: object = None):
        self.calls.append((sql, params))
        if "COUNT" in sql:
            return {"total": 1}
        return {"scene_name": "E2E_CITY"}


class AcceptanceVerticalSliceTest(unittest.TestCase):
    def test_query_builds_parameterized_filter_and_pagination(self) -> None:
        postgres = FakePostgres()
        repository = AcceptanceRepository(postgres)  # type: ignore[arg-type]
        spec = QuerySpec(
            filters=[FilterSpec(field="name", operator="contains", value="城区")],
            sorting=[SortSpec(field="expected_delivery_at", direction="asc")],
            page=2,
            page_size=20,
        )

        rows, total = repository.query_tasks(spec)

        self.assertEqual(total, 1)
        self.assertEqual(rows[0]["name"], "城区测试任务")
        query_sql, query_params = postgres.calls[0]
        self.assertIn("task.dataset_name ILIKE %s", query_sql)
        self.assertEqual(query_params, ["%城区%", 20, 20])

    def test_service_returns_typed_page(self) -> None:
        service = AcceptanceQueryService(AcceptanceRepository(FakePostgres()))  # type: ignore[arg-type]
        page = service.query_tasks(QuerySpec())
        self.assertEqual(page.total, 1)
        self.assertEqual(page.items[0].annotation_submitted, 80)
        self.assertIsNotNone(page.computed_at.tzinfo)

    def test_fastapi_registers_acceptance_routes(self) -> None:
        paths = {route.path for route in create_app().routes}
        self.assertIn("/api/v1/manual-qc/acceptance/tasks/query", paths)
        self.assertIn("/api/v1/manual-qc/acceptance/tasks/{task_id}/breakdown", paths)
        self.assertIn("/api/v1/manual-qc/acceptance/metadata", paths)
        self.assertIn("/api/v1/manual-qc/acceptance/assignment/preview", paths)
        self.assertIn("/api/v1/manual-qc/acceptance/assignment/previews/{preview_id}", paths)

    def test_router_wraps_query_and_breakdown_in_common_response(self) -> None:
        service = AcceptanceQueryService(AcceptanceRepository(FakePostgres()))  # type: ignore[arg-type]

        query_response = query_tasks(QuerySpec(), service)
        self.assertEqual(query_response.code, 0)
        self.assertEqual(query_response.data.total, 1)
        self.assertEqual(query_response.data.items[0].task_code, "E2E-001")

        class BreakdownService:
            def get_daily_breakdown(self, task_id: int):
                self.task_id = task_id
                return [
                    AcceptanceDailyItem(
                        id="1:2026-07-04",
                        stat_date="2026-07-04",
                        annotation_total=100,
                        annotation_submitted=80,
                        annotation_pending=20,
                        acceptance_allocated=20,
                        acceptance_submitted=10,
                        good_allocated=16,
                        good_passed=15,
                        bad_allocated=4,
                        bad_passed=2,
                    )
                ]

        breakdown_service = BreakdownService()
        breakdown_response = get_breakdown(1, "date", breakdown_service)  # type: ignore[arg-type]
        self.assertEqual(breakdown_response.code, 0)
        self.assertEqual(breakdown_response.data[0].annotation_submitted, 80)
        self.assertEqual(breakdown_service.task_id, 1)

        metadata_response = metadata()
        self.assertEqual(metadata_response.data["page_sizes"], [20, 50, 100, 200])

    def test_ratio_sampler_is_deterministic_and_fills_category_shortage(self) -> None:
        plan = plan_ratio_sampling(
            [
                SamplingBucket(id="a", good_available=10, bad_available=2),
                SamplingBucket(id="b", good_available=30, bad_available=3),
            ],
            requested_target=20,
            good_ratio=0.5,
        )

        self.assertEqual(plan.target_count, 20)
        self.assertEqual(plan.planned_good, 15)
        self.assertEqual(plan.planned_bad, 5)
        self.assertEqual(sum(good + bad for good, bad in plan.allocations.values()), 20)
        self.assertIn("Bad 可用量不足", " ".join(plan.warnings))

    def test_assignment_preview_freezes_selection_and_result(self) -> None:
        class PreviewRepository:
            def __init__(self) -> None:
                self.saved: dict[str, object] | None = None

            def get_selection_units(self, task_ids, date_keys):
                self.selection = (task_ids, date_keys)
                return [{
                    "id": "1-date-2026-07-04",
                    "task_id": 1,
                    "task_name": "城区测试任务",
                    "topic": "城区",
                    "scene_name": "E2E_CITY",
                    "stat_date": date(2026, 7, 4),
                    "available": 80,
                    "good_available": 60,
                    "bad_available": 20,
                    "computed_at": datetime(2026, 7, 5, tzinfo=timezone.utc),
                }]

            def save_preview(self, **payload):
                self.saved = payload

        repository = PreviewRepository()
        service = AssignmentPreviewService(repository)  # type: ignore[arg-type]
        response = service.create_preview(
            AssignmentPreviewRequest(
                selection=SelectionSpec(explicit_ids=["1-date-2026-07-04"]),
                rule=AssignmentRuleSpec(target_count=40, good_ratio=0.5),
            ),
            "E2E_REVIEWER",
        )

        self.assertEqual(repository.selection, ([], [(1, "2026-07-04")]))
        self.assertEqual(response.target_count, 40)
        self.assertEqual(response.planned_good + response.planned_bad, 40)
        self.assertIsNotNone(repository.saved)
        self.assertEqual(repository.saved["created_by"], "E2E_REVIEWER")  # type: ignore[index]
        self.assertEqual(repository.saved["result_summary"]["preview_id"], response.preview_id)  # type: ignore[index]

    def test_assignment_preview_rejects_unknown_selection_id(self) -> None:
        service = AssignmentPreviewService(object())  # type: ignore[arg-type]
        with self.assertRaises(InvalidSelectionError):
            service.create_preview(
                AssignmentPreviewRequest(selection=SelectionSpec(explicit_ids=["bad-id"])),
                "E2E_REVIEWER",
            )


if __name__ == "__main__":
    unittest.main()
