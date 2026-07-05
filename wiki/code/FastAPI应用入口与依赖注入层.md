---
title: FastAPI应用入口与依赖注入层
domain: ["ai_dlc", "tooling"]
type: "code_module"
tags: [质检平台, FastAPI, API层, 依赖注入, 健康检查, 单端口部署]
created: 2026-06-21
updated: 2026-07-05
sources: 1
status: active
related_code: ["src/api/app.py"]
code_hash: "sha256:a4ba1984fbe48cdf"
affects_path: []
trigger_keywords: [FastAPI, create_app, deps.py, health, database_health, StaticFiles, CORS]
---

# FastAPI应用入口与依赖注入层

本卡记录当前仓库第一版 `src/api` 后端 API 骨架。它把 [[数据质量门户架构设计]] 中的单端口 FastAPI + Vue 前端部署思想落到当前项目。

## Why

- `create_app()` 是应用工厂，便于测试和未来按环境构造不同 app。
- API 路由统一挂在 `/api/*`，前端静态目录存在时再挂载 `/`。
- CORS 从 [[配置管理公共模块]] 读取，开发态支持 Vite 地址。
- `deps.py` 提供 `get_config()`、`get_database_manager()`、`get_postgres()`，路由层不直接构造基础设施。
- 应用使用 lifespan 关闭共享数据库资源，并注册人工质检验收 Router。

## Who

- 依赖 [[配置管理公共模块]] 提供 API 配置。
- 依赖 [[PostgreSQL数据库公共模块]] 提供数据库健康检查能力。
- 未来 `src/api/routers/*` 的业务路由都应通过 `deps.py` 获取公共能力。

## Where

- `src/api/app.py`：FastAPI app factory、CORS、路由注册、静态前端挂载、shutdown 清理。
- `src/api/deps.py`：API 层依赖注入入口。
- `src/api/routers/health.py`：`/api/health` 与 `/api/health/database`。
- `src/api/schemas/common.py`：统一响应与分页 Schema。
- `src/api/schemas/acceptance.py`：第一纵切 QuerySpec 与任务/日期响应契约。

## 设计约束

- router 只做 HTTP 参数、依赖注入和响应组装，不写业务规则。
- 数据库连接、配置读取、外部服务 client 都必须从 `deps.py` 或应用服务层进入。
- `/api/health` 不触发数据库连接；需要检查数据库时使用 `/api/health/database`。

## 关联卡片

- [[数据质量门户架构设计]]
- [[质检一站式平台长期架构]]
- [[配置管理公共模块]]
- [[PostgreSQL数据库公共模块]]
