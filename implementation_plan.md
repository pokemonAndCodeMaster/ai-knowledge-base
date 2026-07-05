# 质检一站式平台——人工质检验收优先实施方案（v5）

> 更新日期：2026-07-05
> 架构总入口：[[质检一站式平台人工质检模块整体架构]]  
> 动态进度权威：`task.md`  
> 设计演进记录：[[质检一站式平台Phase3前架构评审]]

## 1. 目标

把现有人工质检流程中的验收分配、验收统计、通过/打回和人力管理接入统一 FastAPI + Vue3 门户，同时保留 Delta 平台、中间表刷新、GT 回写和 DMP 记录等既有链路。

本方案追求：

- 用户可以从页面完成“筛选—预览—确认—执行—回查”；
- 采样与判断规则可单测、可 Review；
- 数据库查询、外部调用和业务编排边界清楚；
- 实际结果由任务状态确认，不把接口请求量当作成功量；
- 在当前规模下保持简单，不预建无实际收益的抽象层。

## 0. v5 变更摘要与 Review 边界

本版将人工质检验收中心设为第一个正式纵切，并把 [[质检平台统一数据工作台组件设计]]、[[质检平台可配置卡片布局组件设计]] 提升为前端基础设施，不再允许每个页面自行实现表格和 panel。

Gate 0 已拍板：

1. 不接受商业授权，采用 TanStack Table + TanStack Virtual + 自研 DataWorkbench；
2. API 增加 `QuerySpec`、`SelectionSpec` 和短期 `preview_id`，支持跨页筛选全选、局部排除和稳定执行；
3. preview、公共/个人表格布局、卡片布局和分析卡片统一持久化到 PostgreSQL；
4. 第一纵切先完成“只读验收任务队列 + 按天展开 + 公共表格基础能力”，不等待真实 Delta；
5. 写操作先接 fake Delta，真实联调仍以接口 URL、认证、字段和状态映射补齐为门槛。

完整就绪度和分阶段顺序见 [[人工质检验收中心正式开发就绪度评审]]。

当前已按 [[人工质检验收第一纵切架构枢纽]] 推进：只读任务队列、按日展开、DataWorkbench、DashboardLayout 已有首版；`SelectionSpec + Ratio 配额 + PostgreSQL preview_id + 前端预览 panel` 已形成可重复验证的端到端闭环。后续进入 Group/Personal 策略、验收员约束、fake Delta execute 与回查。

## 2. 非目标

- 不重写人工质检十五步全流程。
- 不替代 Delta 为任务状态权威源。
- 不新建通用操作台账或分布式事务系统。
- 不引入数据库规则解释器、`ports.py`、`adapters/` 或集中式 `domain/` 套件。
- 不在缺少真实资料时编造 Delta URL、认证字段和响应结构。

## 3. 已冻结的架构决策

| 主题 | 当前决定 | 详细卡片 |
|---|---|---|
| 快照粒度 | 日×scene×当日组×标注员；annotator_id 非空 | [[质检平台-综合快照表设计]] |
| 采样 | 快照算配额，任务级表查询具体 task_ids | [[质检平台-验收采样配额与任务选择设计]] |
| 规则 | 代码注册表；规则只计算，不访问 DB/API | [[质检平台-通过打回规则与执行设计]] |
| 数据结构 | 就近定义，稳定复用后上移 | [[质检平台-领域模型层设计]] |
| Repository | manual_qc 共享文件，内部按数据源分小类 | [[质检平台-Repository与数据库访问设计]] |
| Delta | `delta_client.py` 集中调用，状态回查校准 | [[质检平台-Delta调用与状态回查设计]] |
| API | Pydantic/OpenAPI 为契约源；小范围显式选择可提交 ID，大范围执行使用 `SelectionSpec + preview_id` | [[质检平台-API契约与前端交互设计]] |
| 人员 | 一人一项目，组只属于标注员 | [[人工质检-人力管理体系设计]] |
| 权限 | 每业务模块一个等级列 | [[质检平台SSO鉴权接入方案]] |
| 前端 | 明确 preview/executing/executed/refreshing 状态 | [[质检平台-人工质检前端页面与状态设计]] |

## 4. 系统结构

```text
src/
├── config/                         # 已有公共配置
├── database/                       # 已有 PostgreSQL 连接池
├── api/
│   ├── app.py                      # 已有 app factory，需注册 manual_qc
│   ├── auth.py                     # 新增 mock/SSO 身份和权限依赖
│   ├── deps.py                     # 扩展 Repository/Client/Service 工厂
│   └── schemas/
│       ├── acceptance.py
│       └── personnel.py
├── manual_qc/
│   ├── repository.py
│   ├── delta_client.py
│   ├── acceptance/
│   │   ├── models.py               # 仅实际共享结构
│   │   ├── sampler.py
│   │   ├── pass_rules.py
│   │   ├── services/
│   │   │   ├── assignment_service.py
│   │   │   ├── stat_service.py
│   │   │   └── execution_service.py
│   │   └── router.py
│   └── personnel/
│       ├── models.py
│       ├── services/personnel_service.py
│       └── router.py
└── frontend/src/
    ├── shared/
    └── features/manual-qc/
        ├── acceptance/
        └── personnel/
```

## 5. 数据库方案

### 5.1 门户表

`migrations/20260628_personnel_and_permission.sql`：

- `t_personnel`：单项目人员当前属性；
- `t_personnel_op_log`：人员变更历史；
- `t_portal_permission`：验收/人力模块权限等级。

`migrations/20260628_qc_daily_snapshot.sql`：

- `t_qc_daily_snapshot`：个人最小统计行、验收计数和当前结论/执行字段。

两份 migration 已在 PostgreSQL 16.14 空实例顺序执行通过；只使用 PostgreSQL 10+ 已有语法。

### 5.2 上游读取

- Delta 任务查询表：waiting_review、验收人和任务状态；
- `human_inspection_0920`：task 状态时间线、acceptor、operate_time；
- 其他 Good/Bad/题型字段来源需在 Phase 2.5 用真实表字段冻结。

## 6. 后端组件契约

### 6.1 Sampler

输入个人最小统计桶，输出维度级 Good/Bad 配额。初始策略：

- GroupSampler：每组 `min(人数×90, 300)`，Good/Bad 各 50%，按 scene 分配；
- PersonalSampler：每人 90，Good/Bad 各 45，不足补齐；
- RatioSampler：用户给总量和比例。

注册表是策略名称唯一来源。

### 6.2 PassRule

输入完成度和 Good/Bad/整体通过率，输出 PASS/REJECT/PENDING、理由和指标快照。初始规则迁移现有 95%/80% 口径，阈值等值语义必须从旧实现核对。

### 6.3 Repository

```text
PersonnelRepository
SnapshotRepository
AcceptanceTaskRepository
```

使用 `src/database` 命名 connector。人员修改与 op_log、快照批量 UPSERT 需要明确本地事务边界。

### 6.4 DeltaClient

集中封装 `batch_assign`、`batch_review_pass`、`batch_acceptance_pass`、`task_rollback`。真实字段待确认；开发默认 fake/mock。

### 6.5 Service

- AssignmentService：快照→配额→task_ids→preview/execute→回查摘要；
- StatService：任务级记录→最小行聚合→快照 UPSERT/查询；
- ExecutionService：指标→规则结论→人工确认→Delta 调用→状态回查；
- PersonnelService：CRUD、调组、审计和人力统计。

## 7. API 契约

### 7.1 preview/execute 原则

preview 在服务端把选择解析为稳定明细，并持久化短期 `preview_id`。execute 提交 `preview_id + excluded_preview_item_ids + override`，执行前校验归属、权限、过期、数据版本和任务状态，不重新采样；返回成功、跳过、失败数量和 task 级错误摘要。

### 7.2 权限

- VIEW：读统计和 preview；
- OPERATE：执行分配、刷新统计；
- EXECUTE：执行通过/打回；
- MANAGE：人员编辑和调组。

前端隐藏按钮，后端仍强制鉴权。

### 7.3 待冻结字段

- preview 请求的筛选字段和策略参数联合模型；
- task_ids 请求体上限；
- 执行响应错误结构；
- 状态回查查询条件和状态枚举。

## 8. 前端方案

验收模块：AssignView、StatsView、ExecuteView。人力模块：Overview、Annotator、Acceptor、Group。

页面必须展示：preview 生成时间、统计 computed_at、请求/成功/跳过/失败、实际成功量和回查状态。

## 9. 实施阶段

### Phase 2.5：契约冻结

- 获取真实 Delta 接口与任务状态映射；
- 冻结 Pydantic 请求响应；
- 固定三个端到端样例；
- 确认通过/打回执行范围。

### Phase 3A：纯规则

- 实现 sampler.py、pass_rules.py；
- 完成取整、数据不足、阈值边界测试。

### Phase 3B：统计只读链

- 实现 Repository 和 StatService；
- 临时 PostgreSQL 集成测试；
- 提供 stats API。

### Phase 3C：分配闭环

- 实现 assignment preview；
- fake Delta execute；
- 状态回查与实际量刷新；
- 成功/部分失败/重复执行测试。

### Phase 3D：通过打回闭环

- 实现 rule preview；
- EXECUTE 权限与确认；
- 通过/rollback fake 调用和回查。

### Phase 3E：人力与权限

- 人员 CRUD、调组、op_log；
- mock 身份、权限矩阵；
- SSO 只保留真实参数可接入的边界。

### Phase 4：前端

按 [[质检平台-人工质检前端页面与状态设计]] 实现页面与 API；不在后端闭环未稳定前堆完整图表。

### Phase 5：联调

以实际用户链路验证，不以 import、lint 或 Swagger 单独代表端到端完成。

## 10. 测试策略

| 层 | 重点 |
|---|---|
| Sampler/Rule 单测 | 纯函数、边界、解释结果 |
| Repository 集成 | migration、UPSERT、聚合、事务 |
| Service 单测 | fake Repository/DeltaClient、部分失败、重复执行 |
| API 测试 | Schema、401/403、权限等级、错误响应 |
| 前端测试 | preview 失效、按钮权限、部分失败展示 |
| E2E | 分配、统计、通过打回、人力调组完整路径 |

## 11. 完成定义

每个 Phase 完成必须同时满足：

1. 用户路径可运行；
2. 原始风险或需求有对应测试证据；
3. 代码、API、数据库和 Wiki 一致；
4. `task.md`、[[质检平台-实施路线与当前进度]]、`index.md`、`log.md` 已同步；
5. 知识图谱已重新编译，无本轮新增孤岛和断链。

## 12. 当前阻塞

唯一实质外部阻塞是 Delta 真实接口和状态字段资料。其余纯规则、DDL、Repository 结构和 mock API 可以继续推进，但正式写操作联调必须等待真实信息。
