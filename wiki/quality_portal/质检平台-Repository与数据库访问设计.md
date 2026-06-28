---
title: "质检平台-Repository与数据库访问设计"
domain: ["ai_dlc", "tooling"]
type: "synthesis"
tags: ["人工质检", "Repository", "PostgreSQL", "数据库访问", "共享能力"]
created: 2026-06-28
updated: 2026-06-28
sources: 7
status: active
related_code: ["task.md", "migrations/20260628_personnel_and_permission.sql", "migrations/20260628_qc_daily_snapshot.sql", "src/database/postgresql.py", "src/database/manager.py"]
affects_path: ["src/manual_qc/repository.py", "src/database/", "migrations/"]
trigger_keywords: ["Repository", "共享repository", "SnapshotRepository", "PersonnelRepository", "AcceptanceTaskRepository", "SQL"]
---

# 质检平台 Repository 与数据库访问设计

← 总入口：[[质检一站式平台人工质检模块整体架构]]。上层边界：[[质检平台-后端分层与组件边界设计]]。数据模型：[[质检平台-综合快照表设计]]、[[人工质检-人力管理体系设计]]。

## 1. 为什么 Repository 上移到 manual_qc

人工质检的验收、人力、统计和后续预警会重复访问人员、快照和任务级中间表。若每个子组件各写一套 SQL，会出现查询口径和字段映射漂移。

因此保留一个 `src/manual_qc/repository.py` 作为共享入口，但“共享文件”不等于“一个万能类”：按物理数据源和表族拆成多个内聚类。

## 2. 类边界

```text
PersonnelRepository
  ├── list/get/create/update
  ├── change_group/change_project
  ├── append_op_log
  └── get_permission

SnapshotRepository
  ├── upsert_many
  ├── list_minimum_rows
  ├── aggregate_by_group/scene/date
  ├── get_for_rule_evaluation
  └── update_execution_fields

AcceptanceTaskRepository
  ├── fetch_waiting_review_tasks
  ├── fetch_task_statuses
  ├── fetch_records_for_snapshot
  └── fetch_completed_or_rollback_tasks
```

Repository 不包含 `batch_assign`、`task_rollback` 等外部写接口；它们属于 [[质检平台-Delta调用与状态回查设计]] 中的 DeltaClient。

## 3. 公共数据库能力复用

- 连接配置由 `src/config` 读取。
- 连接池由 `DatabaseManager` 和 `PostgresConnector` 创建。
- Repository 构造函数接收指定 connector，不调用 `psycopg2.connect()`。
- 参数化 SQL 防止字符串拼接注入。
- 查询结果在 Repository 边界映射成当前用例所需结构，不把游标对象泄漏给 Service。

## 4. 数据库与连接选择

本地门户表和上游任务查询表可能不在同一 PostgreSQL 实例。Repository 每个类显式持有对应命名 connector：

```text
portal_db  → t_personnel / t_portal_permission / t_qc_daily_snapshot
source_db  → human_inspection_0920 / Delta 查询表
```

`DatabaseManager.postgres(name)` 已支持命名连接。数据库名称和 DSN 只放配置，不写死在业务类。

## 5. 事务边界

当前 `PostgresConnector.execute()` 对单条写语句提交/回滚。以下本地操作需要同一连接事务：

- 修改人员属性 + 写 `t_personnel_op_log`；
- 批量 UPSERT 同一轮快照；
- 更新结论、确认人和确认时间。

Phase 3 若需要多语句原子写，应给公共连接器增加显式 transaction context，或让 Repository 在一次 `connection()` 中统一 commit/rollback。不要在 Service 中散落 `conn.commit()`。

Delta 调用不能加入本地数据库事务，采用 [[质检平台-Delta调用与状态回查设计]] 的状态回查闭环。

## 6. 快照查询口径

物理表只存个人最小行。Repository 提供不同聚合查询，但所有口径都从同一最小行出发：

```sql
-- 示例：按组汇总
SELECT stat_date, scene_name, group_name,
       SUM(annotation_submitted) AS annotation_submitted,
       SUM(acceptance_allocated) AS acceptance_allocated
FROM t_qc_daily_snapshot
WHERE stat_date BETWEEN %s AND %s
GROUP BY stat_date, scene_name, group_name;
```

通过率必须“先求和再相除”，不能平均各行百分比。

## 7. UPSERT 与约束

联合键为 `(stat_date, scene_name, group_name, annotator_id)`。同一轮刷新只更新统计列和 `computed_at/updated_at`，不得误清空已确认的执行字段。

实现时应明确列清单，不使用无差别 `SET row = EXCLUDED.row`。计数约束由 DDL 兜底，Service/Repository 仍需在写入前报告负数或大小关系异常，便于定位上游数据问题。

## 8. 分页与批量

- 人员和快照列表使用 `LIMIT/OFFSET` 起步；数据量证明需要时再升级 cursor。
- task_ids 查询遵守 Delta 单批限制；限制值 `[待人类补充]`。
- 大批 UPSERT 使用 `execute_values` 或分批参数化写入，批大小通过配置控制。
- 不在 API 请求中无上限加载整个历史快照表。

## 9. 测试要求

- 使用临时 PostgreSQL 执行 migration 和 Repository 集成测试。
- 覆盖唯一键 UPSERT、不合法计数、人员修改与日志同事务、组级聚合不重复计数。
- fake Repository 只用于 Service 单测，不能替代真实 SQL 集成验证。

