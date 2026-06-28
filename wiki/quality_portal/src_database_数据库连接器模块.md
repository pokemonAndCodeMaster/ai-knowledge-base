---
title: "src/database/ 数据库连接器模块"
domain: ["ai_dlc", "agent_evaluation", "tooling"]
type: "module_doc"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_common_infra", "原业务域_auto_qa"]
created: 2026-06-28
updated: 2026-06-28
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["src/database/ 数据库连接器模块", "quality_check_pipeline", "common_infra", "auto_qa"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["ab39fcae-f7f4-4a41-85f1-50c5921cc743"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/38_Copied text 1782625236_ab39fcae.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

## NotebookLM 原始元数据快照

```yaml
id: "CM-SRC-DB"
title: "src/database/ 数据库连接器模块"
domain: ["common_infra", "auto_qa"]
type: "code_module"

related_code:
  - "src/database/__init__.py"
  - "src/database/pg_connector.py"

affects_path:
  - "src/database/*"

trigger_keywords: ["PGConnector", "DatabaseConfig", "execute_query", "execute_values_returning", "execute_update", "execute_batch_insert", "query_dataframe"]
tags: ["数据库", "PostgreSQL", "psycopg2"]
summary: "数据库连接器模块，提供 PostgreSQL（PGConnector）原子连接能力，基于 DatabaseConfig 桥梁配置类统一初始化。MongoConnector/BaseConnector/PGManager 及所有向后兼容别名已于 TAG 20260626_000000 清除。"
code_hash:
  src/database/__init__.py: "sha256:bda000665463093b"
  src/database/pg_connector.py: "sha256:50efba6190114f8b"
```
# src/database/ 数据库连接器模块

## Why — 为什么存在

项目需要统一的 PostgreSQL 访问层，隔离连接细节并提供类型安全的查询接口。`PGConnector.execute_query` 内置只读安全检查，防止误用写操作。

> ⚠️ 历史状态：曾存在 `BaseConnector` 抽象基类与 `MongoConnector`/`MongoManager` 实现，因零引用已于 TAG 20260626_000000 删除。`BaseConnector` 的 5 个通用方法（reconnect/is_connected/__enter__/__exit__/__del__）已字节级一致内联至 `PGConnector`。

## Who — 谁调用它

| 调用方 | 使用方式 |
|--------|---------|
| `src/llm/task_repository.py` | `PGConnector.execute_query` / `execute_values_returning` |
| `src/clipinfo/service.py` (ClipService) | `PGConnector.execute_query` |
| `src/data_check/utils/connectors/common_dbserver.py` | 旧版 DBServer 封装 |
| `src/data_check/constants/pgserver.py` | 旧版 PgServer 封装 |
| 其他需 DB 操作的业务模块 | 通过 `DatabaseConfig.from_config(db_key)` 初始化 |

## Where — 模块结构

```
src/database/
├── __init__.py        # 导出 DatabaseConfig, PGConnector
└── pg_connector.py    # PGConnector（含内联的生命周期管理方法）+ DatabaseConfig 桥梁类
```

> 注：`base_connector.py`、`mongo_connector.py` 已删除。`DatabaseConfig` 暂保留在 `pg_connector.py` 中作为从 ConfigManager 到 PGConnector 的桥梁，尚未内化。

## 核心类接口速查

### DatabaseConfig（桥梁配置类，暂保留）

| 工厂方法 | 说明 |
|---------|------|
| `DatabaseConfig(config_str=base64_str)` | 从 Base64 编码的 JSON 创建 |
| `DatabaseConfig(**kwargs)` | 从关键字参数创建 |
| `DatabaseConfig.from_dict(d)` | 从字典创建 |
| `DatabaseConfig.from_yaml(path)` | 从 YAML 文件创建 |
| `DatabaseConfig.from_config(db_key)` | **推荐**：从 `get_database_config(db_key)` 统一配置加载 |

必填字段：`host`, `port`, `database`, `user`, `password`

### PGConnector（PostgreSQL 连接器，含内联方法）

| 方法 | 功能 | 安全检查 |
|------|------|---------|
| `execute_query(sql, params)` | SELECT 查询 → `List[Dict]` | ✅ 禁止 INSERT/UPDATE/DELETE/DROP/TRUNCATE/CREATE/ALTER |
| `query_dataframe(sql, params)` | SELECT → `pd.DataFrame` | ❌ 无安全检查 |
| `execute_update(sql, params)` | UPDATE/DELETE → `int` (影响行数) | — |
| `execute_batch_insert(sql, records)` | 批量 INSERT → `int` | — |
| `execute_values(sql, values)` | psycopg2 execute_values 批量更新 → `int` | — |
| `execute_values_returning(sql, values, template)` | INSERT...RETURNING → `List[Dict]` | — |
| `transaction()` | 上下文管理器：commit/rollback | — |
| `reconnect()` / `is_connected()` | 连接生命周期管理（原 BaseConnector 内联） | — |
| `__enter__` / `__exit__` / `__del__` | 上下文与析构（原 BaseConnector 内联） | — |

⚠️ **关键约束**：`execute_query` 仅允许 SELECT/WITH 开头的 SQL。INSERT...RETURNING 必须用 `execute_values_returning`。

## 配置获取

推荐使用 `DatabaseConfig.from_config(db_key)` 从统一配置加载，内部调用 `get_database_config(db_key)` 获取 `application.database.{db_key}` 配置。

## 已删除对象清单（TAG 20260626_000000）

| 已删除对象 | 原类型 | 原因 |
|-----------|--------|------|
| `src/database/mongo_connector.py` | 文件 | 零引用死代码 |
| `src/database/base_connector.py` | 文件（基类） | 5 个方法已字节级一致内联至 PGConnector |
| `PGManager` | 类（高层封装） | 零引用 |
| `BaseConnector` | 抽象基类 | 已内联 |
| `MongoConnector` / `MongoManager` / `MongoDocFetcher` | 类/别名 | 零引用 |
| `DatabaseConnector` / `DatabaseManager` | 向后兼容别名 | 指向已删除的 PGManager |

> ⚠️ 关联避坑：[[PGConnector接口语义陷阱：execute_query禁止写操作]] — execute_query 硬性只读检查，INSERT...RETURNING 必须用 execute_values_returning
> ⚠️ 关联避坑：[[PF-pg_connector_DatabaseConfig访问陷阱]] — DatabaseConfig 必须用 `.get('database')` 访问，禁止 `.database` 属性访问
> ⚠️ 关联规范：[[全局单例 ConfigManager 使用规范]] — 数据库配置通过 ConfigManager 统一管理
> ⚠️ 关联旧版：[[PgServer数据库连接器]] — DataCheck 旧版仅 PG 的连接器，遗留代码仍使用
> ⚠️ 关联旧版：[[DBServer数据库服务封装]] — DataCheck 旧版 PG+Hive 统一访问层
