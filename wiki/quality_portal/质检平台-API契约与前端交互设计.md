---
title: "质检平台-API契约与前端交互设计"
domain: ["ai_dlc", "tooling"]
type: "synthesis"
tags: ["人工质检", "API契约", "Pydantic", "OpenAPI", "Dry Run", "权限"]
created: 2026-06-28
updated: 2026-06-28
sources: 7
status: active
related_code: ["task.md", "src/api/app.py", "src/api/deps.py", "src/api/schemas/"]
affects_path: ["src/api/", "src/frontend/src/features/manual-qc/"]
trigger_keywords: ["API契约", "preview execute", "Pydantic", "task_ids", "前后端交互", "OpenAPI"]
---

# 质检平台 API 契约与前端交互设计

← 总入口：[[质检一站式平台人工质检模块整体架构]]。相关：[[质检平台-人工质检前端页面与状态设计]]、[[质检平台SSO鉴权接入方案]]、[[质检平台-验收采样配额与任务选择设计]]。

## 1. 契约事实源

HTTP 请求和响应由 `src/api/schemas/*.py` 的 Pydantic 模型定义，FastAPI OpenAPI 是前端契约事实源。内部 dataclass、数据库列和前端 TypeScript 类型不能互相直接替代。

目的：数据库可以增加内部字段而不污染 API；采样算法可以重构而不强迫前端同步内部对象。

## 2. 统一约定

- 路径前缀：`/api/v1/manual-qc/`。
- 时间使用带时区 ISO 8601；统计日期使用 `YYYY-MM-DD`。
- 比率响应使用 0～1 小数，前端负责百分比展示。
- 列表端点必须支持分页；策略列表可不分页。
- 写操作返回结构化 `success_count / skipped_count / failed_count / errors`。
- 错误区分参数错误、权限不足、状态已变化、外部平台失败和内部错误。

## 3. 验收端点

| 方法 | 路径 | 权限 | 用途 |
|---|---|---|---|
| GET | `/acceptance/samplers` | VIEW | 从注册表读取可用采样策略 |
| POST | `/acceptance/assignment/preview` | VIEW | 计算配额并返回具体 task_ids 与汇总 |
| POST | `/acceptance/assignment/execute` | OPERATE | 按 preview task_ids 执行分配 |
| POST | `/acceptance/stats/refresh` | OPERATE | 从任务级记录刷新快照 |
| GET | `/acceptance/stats` | VIEW | 查询快照、趋势和聚合统计 |
| GET | `/acceptance/rules` | VIEW | 从注册表读取判定规则 |
| POST | `/acceptance/execution/preview` | VIEW | 返回 PASS/REJECT/PENDING 和依据 |
| POST | `/acceptance/execution/execute` | EXECUTE | 执行通过/打回 |
| GET | `/acceptance/execution/status` | VIEW | 回查任务状态与实际成功量 |

最终路由数量以实现时的 OpenAPI 为准；若多个端点只是同一资源的不同筛选，不为“凑 11 个端点”重复建接口。

## 4. preview → execute 契约

### preview 请求

包含日期范围、scene、组/人员筛选、策略名和该策略参数。后端校验策略是否存在以及比例、数量范围。

### preview 响应

```text
strategy
filters
summary: expected/good/bad/by_scene/by_annotator
task_ids: [...]              # 本次实际预览出的任务
warnings: [...]              # 数据不足、未进组、供应商冲突等
generated_at
```

### execute 请求

原样携带 preview 的 `task_ids` 和操作者确认信息，不重新运行随机采样。后端逐项重查当前状态，只对仍满足前置状态的任务调用 Delta。

这比持久化 `operation_id` 更符合当前规模，同时保证“看到什么就执行什么”。若未来 task_ids 超过网关请求体上限，再引入短期 preview token，而不是现在提前建表。

## 5. 权限与前端按钮

前端根据 `/me` 或权限响应隐藏/禁用按钮；后端每个写端点仍通过 Depends 校验模块等级。直接构造 HTTP 请求不能绕过权限。

详见 [[质检平台SSO鉴权接入方案]]。

## 6. 状态变化处理

preview 后任务可能被其他人处理。execute 不把这种情况当成系统崩溃：

- 当前状态仍合法：进入执行列表；
- 已经完成目标动作：记为 skipped；
- 状态与目标冲突：记为 failed 并返回 task_id、当前状态和原因；
- Delta 请求失败：保留错误并允许用户刷新状态后重试剩余任务。

页面必须显示请求数、实际发送数、跳过数、失败数，不能只弹“操作成功”。

## 7. 人力端点

| 方法 | 路径 | 权限 | 用途 |
|---|---|---|---|
| GET | `/personnel` | VIEW | 分页、筛选人员 |
| POST | `/personnel` | MANAGE | 新增人员并写 op_log |
| PUT | `/personnel/{id}` | MANAGE | 修改属性并记录 changes |
| POST | `/personnel/{id}/group` | MANAGE | 调组并记录 GROUP_CHANGE |
| GET | `/personnel/ungrouped` | VIEW | 未进组预警 |
| GET | `/personnel/stats` | VIEW | 人力分布和画像统计 |

## 8. 待确认项

- `[待人类补充]` Delta 单批 task_ids 上限及接口超时。
- `[待人类补充]` 真实状态码和值与当前卡片中 66/完成/打回语义的最终映射。
- `[待人类补充]` 是否需要导出接口，还是先由前端导出当前页数据。
