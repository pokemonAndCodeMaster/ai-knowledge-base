---
title: PostgreSQL数据库公共模块
domain: ["ai_dlc", "tooling"]
type: "code_module"
tags: [质检平台, PostgreSQL, 数据库模块, 连接池, DatabaseManager, psycopg2]
created: 2026-06-21
updated: 2026-06-21
sources: 1
status: active
related_code: ["src/database/postgresql.py"]
code_hash: "sha256:561c165c3b3c1ef0"
affects_path: []
trigger_keywords: [PostgreSQL, PostgresConnector, DatabaseManager, fetch_all, fetch_one, execute, health_check, 连接池]
---

# PostgreSQL数据库公共模块

本卡记录当前仓库第一版 `src/database` PostgreSQL 公共模块。它是前后端串联的第一块地基：后端业务模块通过统一连接池访问 PostgreSQL，API 层只拿依赖，不直接管理连接。

## Why

- 将 PostgreSQL 连接策略集中到基础设施层，避免每个业务模块各自创建连接。
- 使用懒初始化连接池：构造 `PostgresConnector` 不会立刻连库，首次查询才创建池。
- 提供小而稳定的查询接口：`fetch_all()`、`fetch_one()`、`execute()`、`health_check()`。
- 用 `RealDictCursor` 返回字典行，方便 FastAPI 直接序列化和业务层转换。

## Who

- 读取 [[配置管理公共模块]] 中的 `PostgresSettings`。
- 通过 `DatabaseManager` 暴露给 [[FastAPI应用入口与依赖注入层]] 的 `deps.py`。
- 未来 `src/llm/`、`src/data_check/`、`src/clipinfo/` 等业务模块应复用本模块，不直接 new 连接池。

## Where

- `src/database/postgresql.py`：`PostgresConnector`、`PostgresHealth`。
- `src/database/manager.py`：`DatabaseManager`、全局 manager 生命周期。
- `tests/test_config_database.py`：验证配置读取、环境变量展开、manager 构造不连库。

## 设计约束

- 路由层不得直接使用 `psycopg2.connect()`。
- 连接池只能由 `PostgresConnector.connect()` 懒创建。
- `execute()` 必须负责事务提交和异常回滚；查询方法不提交事务。
- 健康检查失败只能返回结构化状态，不应导致 API 进程崩溃。

## 关联卡片

- [[配置管理公共模块]]
- [[FastAPI应用入口与依赖注入层]]
- [[质检一站式平台长期架构]]
- [[全栈项目设计模式与实践]]
