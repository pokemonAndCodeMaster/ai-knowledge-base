#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PG_BIN="${PG_BIN:-$(pg_config --bindir)}"
PG_PORT="${PG_PORT:-55439}"
API_PORT="${API_PORT:-58081}"
DATA_DIR="$(mktemp -d /tmp/qc-vertical-XXXXXX)"
LOG_FILE="${DATA_DIR}/postgres.log"
API_LOG_FILE="${DATA_DIR}/api.log"
API_PID=""

cleanup() {
  if [[ -n "${API_PID}" ]]; then
    kill "${API_PID}" >/dev/null 2>&1 || true
    wait "${API_PID}" >/dev/null 2>&1 || true
  fi
  "${PG_BIN}/pg_ctl" -D "${DATA_DIR}" stop -m fast >/dev/null 2>&1 || true
}
trap cleanup EXIT

"${PG_BIN}/initdb" -D "${DATA_DIR}" --auth=trust --no-locale --encoding=UTF8 >/dev/null
"${PG_BIN}/pg_ctl" -D "${DATA_DIR}" -l "${LOG_FILE}" -o "-p ${PG_PORT} -k /tmp" start >/dev/null

psql -h /tmp -p "${PG_PORT}" -d postgres -v ON_ERROR_STOP=1 \
  -f "${ROOT_DIR}/migrations/20260628_personnel_and_permission.sql" \
  -f "${ROOT_DIR}/migrations/20260628_qc_daily_snapshot.sql" \
  -f "${ROOT_DIR}/migrations/20260705_acceptance_vertical_slice.sql" \
  -f "${ROOT_DIR}/tests/fixtures/postgres/acceptance_vertical_slice_seed.sql" >/dev/null

cd "${ROOT_DIR}"
POSTGRES_HOST=localhost POSTGRES_PORT="${PG_PORT}" POSTGRES_DB=postgres POSTGRES_USER="$(id -un)" python - <<'PY'
from src.api.deps import get_acceptance_query_service, get_assignment_preview_service
from src.api.schemas.acceptance import AssignmentPreviewRequest, AssignmentRuleSpec, QuerySpec, SelectionSpec

service = get_acceptance_query_service()
page = service.query_tasks(QuerySpec())
assert page.total == 2, page.total
city = next(item for item in page.items if item.task_code == "E2E-0718")
assert city.annotation_submitted == 3500, city.annotation_submitted
assert [day.submitted for day in city.recent_annotation_days] == [1000, 500, 2000]
daily = service.get_daily_breakdown(city.id)
assert daily is not None and len(daily) == 3
preview_service = get_assignment_preview_service()
preview = preview_service.create_preview(
    AssignmentPreviewRequest(
        selection=SelectionSpec(explicit_ids=[str(city.id)]),
        rule=AssignmentRuleSpec(target_count=900, good_ratio=0.5),
    ),
    "E2E_REVIEWER",
)
assert preview.selected_units == 3, preview.selected_units
assert preview.target_count == 900, preview.target_count
assert preview.planned_good + preview.planned_bad == 900
reloaded = preview_service.get_preview(preview.preview_id, "E2E_REVIEWER")
assert reloaded is not None and reloaded.source_version == preview.source_version
print(f"PostgreSQL vertical slice: 2 tasks, city submitted=3500, daily rows=3, preview={preview.preview_id}")
PY

POSTGRES_HOST=localhost POSTGRES_PORT="${PG_PORT}" POSTGRES_DB=postgres POSTGRES_USER="$(id -un)" \
  python -m uvicorn src.api.app:app --host 127.0.0.1 --port "${API_PORT}" >"${API_LOG_FILE}" 2>&1 &
API_PID=$!
for _ in {1..30}; do
  if curl -fsS "http://127.0.0.1:${API_PORT}/api/health" >/dev/null; then
    break
  fi
  sleep 0.1
done

API_PORT="${API_PORT}" python - <<'PY'
import json
import os
from urllib.request import Request, urlopen

port = os.environ["API_PORT"]
base = f"http://127.0.0.1:{port}/api/v1/manual-qc/acceptance"
payload = {
    "selection": {
        "mode": "filtered",
        "explicit_ids": [],
        "filter_snapshot": {"filters": [], "sorting": [], "page": 1, "page_size": 20},
        "excluded_ids": [],
        "leaf_dimension": "date",
    },
    "rule": {"strategy": "ratio", "target_count": 100, "good_ratio": 0.5},
}
request = Request(
    f"{base}/assignment/preview",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "X-Employee-Id": "E2E_HTTP_REVIEWER"},
    method="POST",
)
with urlopen(request) as response:
    preview = json.load(response)["data"]
assert preview["selected_units"] == 4, preview
assert preview["target_count"] == 100, preview

read_request = Request(
    f"{base}/assignment/previews/{preview['preview_id']}",
    headers={"X-Employee-Id": "E2E_HTTP_REVIEWER"},
)
with urlopen(read_request) as response:
    reloaded = json.load(response)["data"]
assert reloaded["preview_id"] == preview["preview_id"]
print(f"FastAPI preview round-trip: {preview['preview_id']}, units={preview['selected_units']}")
PY

python -m unittest -q tests/test_config_database.py tests/test_acceptance_vertical_slice.py
echo "Acceptance vertical slice backend verification passed."
