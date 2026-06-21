---
title: FastAPI后端API层架构
domain: ["ai_dlc", "tooling"]
type: "module_doc"
tags: [质检平台, FastAPI, API架构, 依赖注入, 路由注册, Schema设计]
created: 2026-06-21
updated: 2026-06-21
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: [FastAPI, app.py, deps.py, router, schema, 依赖注入, StaticFiles, lifespan, API端点]
---

# FastAPI后端API层架构

FastAPI 层负责把质检任务、版本配置、模型评测、数据集管理能力暴露为前端可调用 API，并托管前端静态产物。

## 应用入口

`src/api/app.py` 使用 `create_app()` 工厂函数创建应用。

路由注册顺序必须保持：

1. `/api/tasks`
2. `/api/versions`
3. `/api/evaluations`
4. `/api/datasets`
5. `/api/health`
6. `/` → `StaticFiles(frontend/dist)`，必须晚于 API 路由。

`lifespan` 启动时初始化 `ConfigManager` 单例，确保后续依赖注入可用。前端静态路径来自 `application.yaml -> task_scheduler.server.frontend_path`，默认是 `frontend/dist`。目录不存在时只 warning，不阻断后端启动。

## 依赖注入层

`src/api/deps.py` 是路由层唯一合法依赖入口。路由层禁止直接 `new` 业务类，也禁止直接读取 `os.getenv()`。

| 注入函数 | 返回 | 用途 |
|---|---|---|
| `get_config()` | `Dict[str, Any]` | `application.yaml` 全配置 |
| `get_task_repository()` | `TaskRepository` | 任务 DB 读写 |
| `get_task_creator()` | `TaskCreator` | 任务创建 |
| `get_task_query_service()` | `TaskQueryService` | 聚合查询、进度、吞吐 |

## API 边界

### `/api/tasks`

已实现质检任务主流程：

- 表单创建任务、文件上传创建任务。
- 任务概览统计。
- 任务组概览，按 `task_name` 聚合。
- 任务列表，支持游标分页和筛选。
- 任务详情、通道进度、通道吞吐。
- 批量 kill、清理、恢复、永久删除。

关键约束：

- `/list` 支持 `status`、`channel`、`task_name`、`task_name_exact`、`autosence_id`、`id`、`is_deleted`、`limit`、`cursor`。
- 游标分页 cursor 是 `base64("{created_at}|{id}")`。
- kill 逻辑逐通道更新非终态通道为 `killed`，再由 `_sync_task_status()` 派生任务级状态。
- 禁止直接写任务级 `status='completed'`。

### `/api/versions`

已实现版本配置：

- `POST /versions/`：创建或更新版本配置，`version + channel` 作为联合键。
- `GET /versions/`：列表查询，支持 `version` / `channel` 筛选和 OFFSET 分页。
- `GET /versions/detail`：按 query 参数查详情。
- `GET /versions/{version}/{channel}`：按路径参数查详情。

`config` 与 `processor_params` 是 JSONB 字段，后端保持 dict 传输，前端负责格式化展示。

### 骨架模块

- `/api/evaluations`：模型评测，当前保留创建、报告、列表接口骨架。
- `/api/datasets`：数据集管理，当前保留列表、详情、格式化接口骨架。

## Schema 规范

- 所有 Schema 继承 `BaseModel`。
- 可空字段使用 `Optional`。
- 请求命名：`XxxRequest` / `XxxParams`。
- 响应命名：`XxxResponse` / `XxxItem`。
- 列表响应统一 `items + total`；任务列表因游标分页使用 `items + next_cursor + has_more`。
- 使用 `json_schema_extra` 提供 Swagger 示例。

> 关联经验与规范：[[HUB-前端与API层架构]]、[[LLM任务调度Pipeline全景]]、[[质检一站式平台长期架构]]
