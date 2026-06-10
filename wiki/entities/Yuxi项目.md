---
title: "Yuxi项目"
domain: ["agent_engineering", "knowledge_management"]
type: "entity"
tags: [Yuxi, 语析, 企业知识库, RAG, Milvus, Neo4j, LangGraph]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "Yuxi/backend/"
affects_path: []
trigger_keywords:
  - Yuxi
  - 语析
  - 企业知识库
  - Milvus
  - Neo4j
  - LangGraph
  - PaddleOCR
---

# Yuxi项目（语析）

## 一句话定位

多租户企业知识库与知识图谱智能体开发平台。Python（FastAPI + LangGraph + ARQ异步Worker），存储层为 PostgreSQL + Redis + MinIO + Milvus（向量）+ Neo4j（图）。

## 核心架构：中间件栈 + LangGraph 图编排

> 引用自分析：
> "中间件（Middleware）模式：每个能力域（知识库/文件系统/技能）是可插拔中间件，组合成 Agent 能力栈"

```
SubAgentBackend (LangGraph Agent)
 ├─ FilesystemMiddleware
 ├─ SaveAttachmentsMiddleware
 ├─ KnowledgeBaseMiddleware ← 5工具
 │   - list_kbs / get_mindmap / query_kb
 │   - find_kb_document / open_kb_document
 ├─ SkillsMiddleware
 ├─ SummaryMiddleware（100K token 触发压缩）
 ├─ TodoListMiddleware
 ├─ PatchToolCallsMiddleware
 └─ ModelRetryMiddleware
```

## 关键特性

### 1. 混合检索（Milvus 原生）

> 引用自分析：
> "Yuxi 的 BM25 完全内置于 Milvus，无需外部分词器；Collection Schema 在创建时就绑定了 BM25 Function"

```
vector_search (COSINE, HNSW) + bm25_search (内置)
   → WeightedRanker(0.7, 0.3) → hybrid_search
```

### 2. 图谱增强检索（PPR 算法）

```
entity_hits + triple_hits → seed_weights →
Personalized PageRank (damping=0.85) →
RRF 融合 → 最终结果
```

### 3. 文档解析（三路 OCR）

```
PDF/图片 → MinerU / PaddleX / RapidOCR → Markdown
```

### 4. 语义分块

> 引用自分析：
> "保真关键：Yuxi 的分块在 flush 时带 `title_path`（标题链路，如 `# 第三章|第三节`）作为 chunk header，确保每个 chunk 有自己的上下文路径"

### 5. 代码精准定位

通过 5 工具链实现 token 高效的代码访问：
- `query_kb` → 语义检索返回 chunk
- `find_kb_document` → 文件内 grep 定位
- `open_kb_document` → 按行窗口读取（不加载全文）

## 技术栈

- **后端**: Python, FastAPI, LangGraph, ARQ
- **向量数据库**: Milvus（含内置 BM25）
- **图数据库**: Neo4j / Milvus graph store
- **对象存储**: MinIO
- **关系数据库**: PostgreSQL + Redis
- **前端**: Vue.js
- **文档解析**: MinerU + PaddleX + RapidOCR

## 与其他项目的关系

- 与 [[gbrain项目]] 形成互补：Yuxi 侧重企业级多租户、可视化前端
- 为我们的知识库提供了 PPR 图检索、语义分块、5 工具链的参考
