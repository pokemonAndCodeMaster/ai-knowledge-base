# 质检一站式平台——人工质检验收优先任务看板（v5）

> **最后更新**：2026-07-06（SelectionSpec 与 PostgreSQL 分配预览闭环）
> **接续方式**：下次会话直接打开此文件，从第一个 `⬜` Phase 继续
> **架构总入口**：[[质检一站式平台人工质检模块整体架构]]  
> **详细实施契约**：`implementation_plan.md`

---

## 总体阶段一览

| Phase | 名称 | 交付物 | 状态 |
|-------|------|--------|------|
| 0 | 知识调研 | 通读所有卡片，来源项目结构梳理 | ✅ |
| 1 | 架构设计 | 整体架构、组件边界、业务链路、API、前端、知识卡 | ✅ v4 已重编 |
| 2 | 数据库 DDL | 建表 SQL + 索引 + 约束 + 注释 | ✅ PostgreSQL 16 实跑通过，语法基线 10+ |
| 2.5 | Phase 3 前架构硬化 | 不依赖 Delta 的基础契约已完成；真实写操作契约待补 | 🚧 |
| 2.6 | 正式开发 Gate 0 | 开源表格、Query/Selection、PostgreSQL preview、UI 配置 | ✅ 当前版 |
| 3 | 后端 Python 骨架 | 查询、SelectionSpec、Ratio 配额、PostgreSQL preview | 🚧 分配预览已落 |
| 4 | 前端 Vue3 与共享工作台 | AppShell + DataWorkbench + DashboardLayout + 验收预览 | 🚧 分配预览已落 |
| 5 | 联调验证 | PostgreSQL、FastAPI HTTP、Vue 行为与构建 | 🚧 预览链路已通 |

---

## Phase 0 — 知识调研 ✅

**结论**（后续 Phase 引用）：
- `src/config/` 和 `src/database/` 已在本仓库，直接复用
- 抽样策略：`GroupSampler`（每组 min(人数×90,300)，Good/Bad各50%）+ `PersonalSampler`（每人90条）
- 通过规则：Good>95% + Bad>80%，前置条件验收数≥应抽数×0.95
- 题型：driving_behavior / time_range / target_scene

---

## Phase 1 — 架构设计 ✅

### 确认的关键架构决策

| 决策 | 选择 | 理由 |
|------|------|------|
| Repository 设计 | `manual_qc/repository.py` 共享入口，内部按数据源分 Personnel/Snapshot/Task 类 | 复用少量表和查询口径，同时避免万能大类 |
| Delta 调用 | `manual_qc/delta_client.py` | 外部平台调用与数据库访问分开，名称直白，不引入 adapters |
| 采样/规则引擎 | 分别放 `sampler.py` / `pass_rules.py`，代码注册表是名称唯一来源 | 不超 3～5 种策略，git 可审计，规则可纯单测 |
| 快照表 | 合并标注+验收为一张 `t_qc_daily_snapshot` | 个人最小行负责计数/配额/判断；task 表负责具体执行对象 |
| 人力表 | 3 张（personnel + op_log + permission）| 一人一行平铺，7 张表是过设计 |
| 权限设计 | 一人一行，每个业务模块一个权限等级列 | 模块内新功能归入既有等级；新增独立模块才加列 |
| 规则是否入 DB | 否，代码注册表即可 | 规则是业务逻辑，git 版控+code review足矣 |
| 数据结构组织 | 就近定义、稳定复用后上移；不预设独立 domain 目录 | 避免集中式类型垃圾场，前后端契约由 Pydantic/OpenAPI 承担 |
| 外部结果 | execute 前重查状态，调用后通过现有中间表/Delta 状态回查 | 接受人工流程允许延迟和部分失败，以实际状态而非请求量为准 |

### 知识库卡片（Phase 1 产出）

| 卡片 | 路径 | 状态 |
|------|------|------|
| 整体架构入口 | `wiki/synthesis/质检一站式平台人工质检模块整体架构.md` | ✅ |
| 后端分层与组件边界 | `wiki/quality_portal/质检平台-后端分层与组件边界设计.md` | ✅ |
| API 与前端交互 | `wiki/quality_portal/质检平台-API契约与前端交互设计.md` | ✅ |
| 前端页面与状态 | `wiki/quality_portal/质检平台-人工质检前端页面与状态设计.md` | ✅ |
| Repository 与数据库 | `wiki/quality_portal/质检平台-Repository与数据库访问设计.md` | ✅ |
| Delta 与状态回查 | `wiki/quality_portal/质检平台-Delta调用与状态回查设计.md` | ✅，真实字段待补 |
| 综合快照 | `wiki/quality_portal/质检平台-综合快照表设计.md` | ✅ |
| 验收采样 | `wiki/quality_portal/质检平台-验收采样配额与任务选择设计.md` | ✅ |
| 通过打回 | `wiki/quality_portal/质检平台-通过打回规则与执行设计.md` | ✅ |
| 人力管理 | `wiki/quality_portal/人工质检-人力管理体系设计.md` | ✅ |
| 权限与 SSO | `wiki/quality_portal/质检平台SSO鉴权接入方案.md` | ✅ 设计；真实 SSO 参数待补 |
| 数据结构组织 | `wiki/quality_portal/质检平台-领域模型层设计.md` | ✅ |
| scene_name | `wiki/quality_portal/质检平台-scene_name概念.md` | ✅ |
| 实施路线与进度 | `wiki/quality_portal/质检平台-实施路线与当前进度.md` | ✅ |

---

## Phase 2 — 数据库 DDL ✅

### 产出物

| 文件 | 内容 | 执行顺序 |
|------|------|---------|
| [migrations/20260628_personnel_and_permission.sql](file:///home/yyh/project/ai-knowledge-base/migrations/20260628_personnel_and_permission.sql) | t_personnel + t_personnel_op_log + t_portal_permission（3张）| 1 |
| [migrations/20260628_qc_daily_snapshot.sql](file:///home/yyh/project/ai-knowledge-base/migrations/20260628_qc_daily_snapshot.sql) | t_qc_daily_snapshot（合并标注+验收，含执行结论）| 2 |

> ⚠️ `20260628_acceptance_stat_snapshot.sql` 已删除，被 `20260628_qc_daily_snapshot.sql` 替代

> 2026-06-28 第二轮复核：快照粒度已冻结为 `(stat_date, scene_name, group_name, annotator_id)`，每行对应一名标注员在某日、某 scene、当日组别下的最小统计单元；不再写 `annotator_id IS NULL` 的组汇总行。DDL 使用 PostgreSQL 10+ 已有语法，并已在一次性 PostgreSQL 16.14 实例顺序执行通过。详见 [[质检一站式平台Phase3前架构评审]]。

---

## Phase 2.5 — Phase 3 前架构硬化 ⏳

- [ ] 明确 Delta 查询/分配/通过/打回接口、认证方式和字段映射
- [x] 接受现状：调用后通过任务级中间表/Delta 状态回查真实结果，不新增通用操作台账
- [x] 冻结快照最小粒度；组、任务、日期均作为可直接聚合的维度列
- [x] 人员改为同一时刻只属于一个项目，`projects TEXT[]` 改为 `project_name VARCHAR`
- [x] 权限改为模块级等级列：验收 NONE/VIEW/OPERATE/EXECUTE，人力 NONE/VIEW/MANAGE
- [x] 取消强制 `domain/ports/adapters` 目录：数据结构就近定义，Delta 调用使用直白的 `delta_client.py`
- [ ] 冻结 preview/execute 简化契约：execute 携带 preview 返回的 task_ids，后端执行前重查状态
- [x] 修订 DDL 并在临时 PostgreSQL 16.14 实例实跑，migration、正常插入、UPSERT 与非法计数约束均符合预期
- [ ] 用三个示例验证：全部成功、部分失败后状态回查、重复点击时跳过已完成任务
- [x] 总卡、组件分卡、实施计划、动态看板和双向链接完成重编

---

## Phase 3 — 后端 Python 骨架 🚧

> 进入本阶段前先完成 [[人工质检验收中心正式开发就绪度评审]] 的 Gate 0。旧计划中“execute 直接携带全部 preview task_ids”只适合小范围显式选择；跨页全选与复杂筛选改用 `SelectionSpec + preview_id`。

当前第一纵切已完成查询 Schema、参数化 Repository、任务聚合、日期展开、SelectionSpec、Ratio 配额、PostgreSQL preview 写入/读回和前端预览。Group/Personal 策略、execute、权限和真实 Delta 仍未开始。

### 目录结构（最终版）

```
src/manual_qc/
├── __init__.py                         ✅ 已创建
│
├── acceptance/
│   ├── __init__.py                     ✅ 已创建
│   ├── models.py                       ⬜  可选；仅在出现稳定复用结构时创建
│   ├── sampler.py                      ⬜  GroupSampler / PersonalSampler / RatioSampler + SAMPLER_REGISTRY
│   ├── pass_rules.py                   ⬜  RateBasedPassRule / StrictRateRule + RULE_REGISTRY
│   ├── services/
│   │   ├── __init__.py                 ⬜
│   │   ├── assignment_service.py       ⬜  preview_assignment / execute_assignment / validate_supplier_conflict
│   │   ├── stat_service.py             ⬜  compute_annotation_stats / refresh_acceptance_stats / get_snapshot
│   │   └── execution_service.py        ⬜  preview_execution / confirm_conclusion / execute
│   └── router.py                       ⬜  /acceptance/* 11 个端点
│
├── personnel/
│   ├── __init__.py                     ⬜
│   ├── models.py                       ⬜  Personnel / PersonnelFilter（仅人力模块使用）
│   ├── services/
│   │   ├── __init__.py                 ⬜
│   │   └── personnel_service.py        ⬜  CRUD + get_ungrouped / group_stats
│   └── router.py                       ⬜  /personnel/* CRUD + 分组管理端点
│
├── repository.py                      ⬜  共享入口，内部按表/数据源分为多个内聚类
│   ├── PersonnelRepository            # 人员、操作日志、权限
│   ├── AcceptanceTaskRepository       # 查询任务级中间表/Delta 查询表
│   │   ├── fetch_waiting_review()
│   │   └── fetch_task_status()
│   └── SnapshotRepository             # 读写 t_qc_daily_snapshot
│       ├── upsert_snapshot()
│       ├── get_snapshot()
│       ├── list_snapshots()
│       └── mark_executed()
└── delta_client.py                    ⬜  调用现有 Delta 平台接口；不是数据库连接层
    ├── batch_assign()
    ├── batch_review_pass()
    ├── batch_acceptance_pass()
    └── task_rollback()

src/api/
├── app.py                             ⬜  FastAPI 实例 + router 注册 + StaticFiles
├── auth.py                            ⬜  mock 身份 + 模块等级权限；预留真实 SSO
├── deps.py                            ⬜  Service 依赖注入工厂
└── schemas/
    ├── acceptance.py                  ⬜  全部 Request/Response Pydantic Schema
    └── personnel.py                   ⬜  人力管理 Schema
```

### Step 执行顺序（按依赖顺序）

```
Step 3.1  acceptance/models.py + sampler.py + pass_rules.py  ← 纯 Python；类型就近定义、复用后上移
Step 3.2  src/manual_qc/repository.py + delta_client.py       ← 复用 src/database 与 src/config
Step 3.3  src/manual_qc/acceptance/services/                  ← 编排统计、接口调用和状态回查
Step 3.4  src/manual_qc/personnel/                            ← 人力模型、Service、Router
Step 3.5  src/api/                            ← 依赖 services
Step 3.6  tests/                              ← 单元测试（sampler + pass_rules）
```

### Phase 3 完成标准

- [ ] `python -c "from src.manual_qc.acceptance.services.assignment_service import AssignmentService"` 成功
- [ ] `uvicorn src.api.app:app` 启动，`GET /api/health` 返回 200
- [ ] `/docs` 显示所有端点
- [ ] `python -m pytest tests/test_sampler.py` 通过
- [ ] `python -m pytest tests/test_pass_rules.py` 通过

---

## Phase 4 — 前端 Vue3 骨架 🚧

### 目录结构（4 页签）

```
src/frontend/src/
├── shared/
│   ├── api/index.ts         axios 实例
│   ├── types/common.ts      PageResponse / TimeRange
│   └── components/
│       ├── FilterBar.vue
│       ├── StatusTag.vue
│       ├── ConfirmDialog.vue
│       └── charts/BaseChart.vue
│
└── features/manual-qc/
    ├── acceptance/          验收模块（分配/统计/执行三页签）
    │   ├── types.ts
    │   ├── api.ts
    │   └── views/
    │       ├── AcceptanceLayout.vue
    │       ├── AssignView.vue
    │       ├── StatsView.vue
    │       └── ExecuteView.vue
    ├── personnel/           人力管理模块（概览/标注员/验收员/分组四页签）
    │   ├── types.ts
    │   ├── api.ts
    │   └── views/
    │       ├── PersonnelLayout.vue
    │       ├── OverviewView.vue
    │       ├── AnnotatorView.vue
    │       ├── AcceptorView.vue
    │       └── GroupView.vue
    └── routes.ts            /manual-qc/* 路由注册
```

### Phase 4 完成标准

- [ ] `npm run dev` 无报错
- [ ] 侧边栏「人工质检 → 验收 / 人力管理」可点击
- [ ] 验收：三页签骨架渲染（分配/统计/执行）
- [ ] 人力：四页签骨架渲染（概览/标注员/验收员/分组管理）
- [ ] 采样策略下拉框从后端 `/samplers` 接口读取

---

## Phase 5 — 联调验证 ⬜

### 接口验证清单

```
GET  /api/v1/manual-qc/acceptance/samplers           → 策略列表
GET  /api/v1/manual-qc/acceptance/rules              → 规则列表
POST /api/v1/manual-qc/acceptance/assignment/preview → Dry Run 分配预览
POST /api/v1/manual-qc/acceptance/assignment/execute → 执行分配
POST /api/v1/manual-qc/acceptance/stats/compute      → 触发统计计算
GET  /api/v1/manual-qc/acceptance/stats              → 查询快照
POST /api/v1/manual-qc/acceptance/execution/preview  → 通过/打回预览
POST /api/v1/manual-qc/acceptance/execution/confirm  → 确认结论
POST /api/v1/manual-qc/acceptance/execution/execute  → 执行通过/打回
GET  /api/v1/manual-qc/personnel                     → 人员列表
POST /api/v1/manual-qc/personnel/{id}/group          → 修改组别
```

### 前后端联调路径

- [ ] 分配页：选规则→预览→确认警告→执行→快照表更新
- [ ] 统计页：触发计算→表格更新→图表更新→导出
- [ ] 执行页：预览结论→确认→执行→is_executed=TRUE
- [ ] 人力页：列表/搜索/修改组别/未进组预警

---

## 当前待补充（Phase 3 写操作联调前完成）

- [ ] Delta 接口 URL、认证、请求/响应、单批上限和错误码
- [ ] waiting_review、已完成、打回后状态的实际字段和值
- [ ] 通过/打回最终执行范围
- [ ] 真实公司 SSO 参数（不阻塞 mock 模式后端开发）

---

## 推荐下一步

> **立即进行**：以 [[人工质检验收第一纵切架构枢纽]] 为 Review 入口，补齐 Group/Personal 策略、验收员与供应商约束、preview 局部排除/覆盖；随后实现 fake Delta execute 与回查。并行完善 DataWorkbench 筛选编辑和布局持久化。
