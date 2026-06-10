---
title: "CodeGraph存储层"
domain: ["code_intelligence"]
type: "code_module"
tags: [CodeGraph, SQLite, FTS5, 数据库, BM25, 全文搜索]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "codegraph/src/db/index.ts"
  - "codegraph/src/db/queries.ts"
  - "codegraph/src/db/sqlite-adapter.ts"
  - "codegraph/src/db/migrations.ts"
code_hash: ""
affects_path: []
trigger_keywords:
  - SQLite
  - FTS5
  - BM25
  - DatabaseConnection
  - QueryBuilder
---

# CodeGraph存储层 (Storage Layer)

## 职责

将提取的 nodes / edges / files 持久化到本地 SQLite 数据库，并通过 FTS5 全文搜索引擎提供高性能的符号检索。

## 核心组件

- **DatabaseConnection** (`index.ts`)：数据库连接管理，支持 `better-sqlite3` (native) 和 `node-sqlite3-wasm` (WASM fallback)
- **QueryBuilder** (`queries.ts`)：预编译 SQL 语句封装，包含 `searchNodesFTS` (BM25)、`findNodesByExactName` (co-location boost)
- **sqlite-adapter.ts**：原生 vs WASM 双后端透明切换
- **schema.sql**：数据库表结构定义（nodes, edges, files 三张核心表）
- **migrations.ts**：schema 版本迁移

## 关键设计

- **WAL 模式**：并发读不阻塞写，`codegraph status` 会显示当前 Journal 模式
- **FTS5 全文搜索**：基于 BM25 的符号名搜索，支持 `codegraph_search` 工具
- **Co-location Boost**：`findNodesByExactName` 对同文件/同目录的符号给予额外加分

## 数据模型

```
nodes: id, name, kind, qualified_name, file_path, start_line, end_line, source_code, ...
edges: source_id, target_id, kind, provenance, metadata
files: path, hash, size, mtime, language
```

## 与其他层的关系

- 上游：接收 [[CodeGraph提取层]] 产出的符号和关系
- 下游：被 [[CodeGraph图遍历层]] 查询调用
