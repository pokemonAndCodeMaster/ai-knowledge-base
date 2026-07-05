BEGIN;

DELETE FROM t_qc_daily_snapshot WHERE scene_name LIKE 'E2E_%';
DELETE FROM t_qc_delivery_task WHERE scene_name LIKE 'E2E_%';
DELETE FROM t_personnel WHERE employee_id LIKE 'E2E_%';

INSERT INTO t_personnel
    (employee_id, name, role, level, supplier, project_name, current_group, status, join_date)
VALUES
    ('E2E_A01', '测试标注员甲', 'ANNOTATOR', 'STANDARD', '供应商甲', '验收纵切', '城区A组', 'ACTIVE', DATE '2026-01-01'),
    ('E2E_A02', '测试标注员乙', 'ANNOTATOR', 'SENIOR', '供应商乙', '验收纵切', '城区B组', 'ACTIVE', DATE '2026-01-01'),
    ('E2E_A03', '测试标注员丙', 'ANNOTATOR', 'STANDARD', '供应商甲', '验收纵切', '园区A组', 'ACTIVE', DATE '2026-01-01');

INSERT INTO t_qc_delivery_task
    (task_code, dataset_name, scene_name, topic, priority, expected_delivery_at, expected_quantity, status, owner_employee_id)
VALUES
    ('E2E-0718', '城区路口交互第三批', 'E2E_CITY_INTERACTION', '城区', 'P0', DATE '2026-07-18', 12000, 'ACCEPTANCE_RUNNING', 'qa001'),
    ('E2E-0725', '园区窄路会车', 'E2E_PARK_NARROW', '园区', 'P1', DATE '2026-07-25', 8000, 'ACCEPTANCE_PENDING', 'qa002');

INSERT INTO t_qc_daily_snapshot
    (stat_date, scene_name, group_name, annotator_id,
     annotation_total, annotation_submitted, annotation_pending, option_annotation,
     acceptance_allocated, acceptance_submitted,
     good_allocated, good_passed, bad_allocated, bad_passed, option_acceptance,
     conclusion, is_executed)
SELECT DATE '2026-07-01', 'E2E_CITY_INTERACTION', '城区A组', id,
       2500, 2000, 500, '{"GOOD":1700,"BAD_RULE":300}',
       400, 360, 330, 318, 70, 42, '{}', 'PENDING', FALSE
FROM t_personnel WHERE employee_id='E2E_A01';

INSERT INTO t_qc_daily_snapshot
    (stat_date, scene_name, group_name, annotator_id,
     annotation_total, annotation_submitted, annotation_pending, option_annotation,
     acceptance_allocated, acceptance_submitted,
     good_allocated, good_passed, bad_allocated, bad_passed, option_acceptance,
     conclusion, is_executed)
SELECT DATE '2026-07-03', 'E2E_CITY_INTERACTION', '城区B组', id,
       1800, 500, 1300, '{"GOOD":420,"BAD_RULE":80}',
       100, 90, 82, 79, 18, 11, '{}', 'PENDING', FALSE
FROM t_personnel WHERE employee_id='E2E_A02';

INSERT INTO t_qc_daily_snapshot
    (stat_date, scene_name, group_name, annotator_id,
     annotation_total, annotation_submitted, annotation_pending, option_annotation,
     acceptance_allocated, acceptance_submitted,
     good_allocated, good_passed, bad_allocated, bad_passed, option_acceptance,
     conclusion, is_executed)
SELECT DATE '2026-07-04', 'E2E_CITY_INTERACTION', '城区A组', id,
       2000, 1000, 1000, '{"GOOD":760,"BAD_RULE":240}',
       200, 180, 152, 145, 48, 26, '{}', 'PENDING', FALSE
FROM t_personnel WHERE employee_id='E2E_A01';

INSERT INTO t_qc_daily_snapshot
    (stat_date, scene_name, group_name, annotator_id,
     annotation_total, annotation_submitted, annotation_pending, option_annotation,
     acceptance_allocated, acceptance_submitted,
     good_allocated, good_passed, bad_allocated, bad_passed, option_acceptance,
     conclusion, is_executed)
SELECT DATE '2026-07-04', 'E2E_PARK_NARROW', '园区A组', id,
       8000, 2100, 5900, '{"GOOD":1600,"BAD_RULE":500}',
       0, 0, 0, 0, 0, 0, '{}', NULL, FALSE
FROM t_personnel WHERE employee_id='E2E_A03';

COMMIT;
