---
title: "质检一站式平台 Phase 3 前架构评审"
domain: ["ai_dlc", "tooling"]
type: "synthesis"
tags: ["质检平台", "架构评审", "人工质检", "数据建模", "状态回查", "渐进式设计"]
created: 2026-06-28
updated: 2026-06-28
sources: 15
status: active
related_code: ["task.md", "implementation_plan.md", "migrations/20260628_personnel_and_permission.sql", "migrations/20260628_qc_daily_snapshot.sql", "src/manual_qc/", "src/api/app.py", "src/api/deps.py", "src/database/postgresql.py"]
affects_path: ["src/manual_qc/", "src/api/", "migrations/"]
trigger_keywords: ["Phase 3", "架构评审", "快照表", "采样依据", "状态回查", "preview execute", "领域模型", "repository"]
---

# 质检一站式平台 Phase 3 前架构评审

本卡记录两轮架构评审后的当前结论。第二轮以现有人工质检流程为约束，撤回第一轮中过重的操作台账、ports/adapters 和集中式 domain 目录建议。

当前定稿入口：[[质检一站式平台人工质检模块整体架构]]。实施状态：[[质检平台-实施路线与当前进度]]。

关联：[[质检平台-综合快照表设计]]、[[质检平台-采样与规则引擎设计]]、[[质检平台-领域模型层设计]]、[[人工质检-人力管理体系设计]]、[[人工质检-⑧验收分配]]、[[人工质检-⑨批量通过打回]]、[[人工质检-⑪中间表更新]]。

## 当前总体结论

保留 API → Service → Repository/外部 Client 的简单分层，以及代码注册表、Dry Run/Wet Run 和综合快照表。实现遵循三条原则：

1. 接受现有 Delta 平台接口和异步状态刷新机制，不把人工质检改造成强事务系统。
2. 数据结构就近定义，至少两个组件稳定复用后再上移，不预建类型仓库。
3. 快照负责统计和计算依据；任务级中间表/Delta 表负责定位具体 clip/task 并确认实际执行结果。

## 1. 数据结构与 domain 目录

### 当前决定

不创建 `acceptance/domain/` 作为所有数据结构的集中目录。

Python 中 `domain/` 常见于领域驱动设计，但不是语言或 FastAPI 的标准要求。小型业务模块如果先建一个全局 `models.py`，容易出现：

- 采样、统计、HTTP、数据库行模型全部堆在一起；
- 修改一个共享类迫使无关组件同步变化；
- 为了“统一”而暴露本应私有的字段。

本项目采用局部优先：

```text
acceptance/sampler.py       # 采样器私有配置/结果先定义在这里
acceptance/pass_rules.py    # 判定规则私有输入/结果先定义在这里
acceptance/models.py        # 仅放 acceptance 内多个组件共同依赖的稳定结构
personnel/models.py         # 仅服务人力模块
api/schemas/acceptance.py   # 前后端 HTTP 契约（Pydantic）
```

后端 dataclass 不是前端直接使用的类型。前端交互由 Pydantic Schema 生成 OpenAPI，再由前端手写或生成 TypeScript 类型。Domain/内部模型与 API Schema 可以字段相近，但职责不同。

## 2. 快照是采样计算依据，但不是 clip 明细表

修正第一轮“快照不能作为采样事实源”的绝对表述。

`t_qc_daily_snapshot` 已保存最小统计单元及其 Good/Bad、选项、提交和验收计数，足以计算每个维度应该抽多少。真正执行分配时，仍需根据日期、scene、组、标注员和 Good/Bad 条件，到任务级中间表或 Delta 表查询具体 `task_id/clip_id`，再调用平台接口。

```text
快照计数 → 计算每个最小单元的抽样配额
        → 任务级表查询符合条件的 task_ids
        → 前端预览
        → Delta API 执行分配
        → 回查 task 状态
        → 快照 acceptance_allocated 刷新为实际成功量
```

## 3. 快照粒度

唯一粒度固定为：

```text
stat_date × scene_name × group_name × annotator_id
```

- `annotator_id` 必须有值，每行对应一名标注员的最小统计单元。
- `group_name` 记录标注员在 `stat_date` 当天的组别，后续调组不改历史。
- 组级、任务级、日期级统计直接 `GROUP BY` 聚合个人行。
- 不保存 `annotator_id IS NULL` 的重复组汇总行，避免个人行和汇总行重复计数。
- `conclusion/is_executed` 可以继续随最小行保存，以适配当前人工流程；不另造通用操作台账。

## 4. 预览与执行：权限和内容一致性是两件事

按钮权限解决“谁能操作”：无权限的人前端看不到按钮，同时后端接口必须再次鉴权，不能只依赖前端隐藏。

预览一致性解决“执行的是不是刚才看到的那些任务”。当前不需要 `operation_id` 表，采用简单契约即可：

1. preview 返回选中的 `task_ids` 和统计摘要；
2. execute 请求携带这批原始 `task_ids`，不重新随机采样；
3. 后端执行前重查状态，只处理仍处于 `waiting_review` 等目标前置状态的任务；
4. 已被别人处理或已完成的任务记为跳过，并返回成功/跳过/失败数量。

## 5. 外部 Delta 调用与状态回查

“外部接口不是本地事务”只表示：调用 Delta 成功与写本地快照不是同一个数据库动作，二者可能一个成功、一个失败。当前系统已有适合的最终校准来源：

- [[人工质检-⑧验收分配]]：任务状态 66 `waiting_review`，通过 `batch_assign`、`batch_review_pass` 执行。
- [[人工质检-⑨批量通过打回]]：通过后进入已完成；打回通过两次 `task_rollback` 退回筛选。
- [[人工质检-⑩状态刷新与GT回写]]：每 30 分钟同步 Delta 状态。
- [[人工质检-⑪中间表更新]]：每 6 小时写 `human_inspection_0920`，其中包含 task_id、acceptor、MergedTaskStatus 和操作时间。

因此本项目采用“发起操作 + 状态回查 + 快照校准”：接口响应只作为即时提示，真实成功量以后续任务状态为准。

“幂等”的朴素含义是：用户重复点一次，不应把已经完成的任务再做一遍。这里无需新框架，只需执行前按 task_id 查询状态，跳过已不在前置状态的任务。

## 6. DDL 修订

两份 DDL 以 PostgreSQL 10+ 为兼容基线，避免 identity、generated column、`NULLS NOT DISTINCT` 等较新语法：

- 快照 `annotator_id` 改为 `NOT NULL`，唯一约束只使用普通列。
- 增加非负、提交量、验收量、通过量和执行字段一致性检查。
- `acceptance_allocated` 明确表示状态回查后确认的实际成功分配量。
- 人员 `projects TEXT[]` 改为单值 `project_name VARCHAR(64)`。
- 增加角色/层级、分组、单价和离场日期约束。

## 7. 权限模型

采用“每个业务模块一个等级列”，不是每个按钮一个布尔列：

```text
acceptance_access: NONE / VIEW / OPERATE / EXECUTE
personnel_access:  NONE / VIEW / MANAGE
```

- 新增“导出统计”等验收内功能时，映射到 VIEW，无需改表。
- 新增“重新分配”等操作时，映射到 OPERATE，无需改表。
- 新增完全独立的模块时，才增加一个新的模块权限列。
- 若未来出现同模块内互不包含的复杂权限，再升级 capability/RBAC；当前不提前建设。

## 8. 注册表与重复事实源

重复不是前后端注册表重复，而是后端内部同时维护两份策略名称：

```python
class SamplerName(Enum):
    BY_GROUP = "by_group"

SAMPLER_REGISTRY = {
    "by_group": GroupSampler(),
}
```

新增策略时若只改一处，就会出现 API 接受但找不到实现，或实现已注册但请求校验不接受。当前选择：

- `SAMPLER_REGISTRY`、`RULE_REGISTRY` 是策略名称唯一事实源；
- API 请求接收字符串，Service 通过 `get_sampler/get_rule` 校验；
- `QuestionType`、人员角色、结论状态等真正封闭的业务集合仍使用 Enum；
- `SamplingConfig` 只定义一次；`target_count` 明确表示最终目标条数，不再同时表示组员数。

## 9. Repository、Delta Client 与公共数据库能力

保留 `src/manual_qc/repository.py` 作为人工质检共享数据访问入口，因为多个子功能确实复用少量表。文件内部按数据源拆成小类：

```text
PersonnelRepository   # t_personnel / op_log / permission
SnapshotRepository    # t_qc_daily_snapshot
AcceptanceTaskRepository # 查询任务级中间表/Delta 查询表
```

这些类共享 `src/database/PostgresConnector`，不自行创建连接或读取数据库配置。

不引入 `ports.py` 和 `adapters/` 目录。第一轮所说的 adapter 本意只是“把 Delta HTTP 调用包起来”，并非已有两个不兼容系统需要转换；这里直接命名为 `src/manual_qc/delta_client.py`，集中放 `batch_assign`、`batch_review_pass`、`batch_acceptance_pass`、`task_rollback`，语义更直观。

Repository 只负责查询/写数据库，`DeltaClient` 只负责调用平台接口，Service 负责编排二者。

## 10. 下一步

1. 在临时 PostgreSQL 实例执行两份 migration，并验证约束和典型 UPSERT。
2. 补齐 Delta 接口的实际 URL、认证、请求/响应字段和状态码映射。
3. 冻结 preview/execute 请求响应：同一批 task_ids、执行前状态重查、成功/跳过/失败计数。
4. 先实现 sampler、pass_rules 及边界测试，再实现 Repository、DeltaClient 和 Service。

## 11. DDL 实跑证据

2026-06-28 使用本机 PostgreSQL 16.14 建立一次性空实例，按顺序执行：

1. `migrations/20260628_personnel_and_permission.sql`：退出码 0。
2. `migrations/20260628_qc_daily_snapshot.sql`：退出码 0。
3. 插入单项目标注员、模块等级权限和合法快照：成功。
4. 使用联合唯一键执行 `ON CONFLICT ... DO UPDATE`：成功。
5. 插入 `annotation_submitted > annotation_total` 的非法快照：被 `ck_annotation_counts_order` 拒绝，符合预期。

测试实例已停止。当前环境只有 PostgreSQL 16，因此没有对 PostgreSQL 10 二进制做实跑；DDL 有意未使用 10 之后才出现的 identity、generated column、`NULLS NOT DISTINCT` 等语法。
