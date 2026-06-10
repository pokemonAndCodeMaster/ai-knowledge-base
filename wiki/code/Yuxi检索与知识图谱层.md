---
title: "Yuxi检索与知识图谱层"
domain: ["knowledge_management"]
type: "code_module"
tags: [Yuxi, Milvus, PPR, 混合检索, 知识图谱, Neo4j]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "Yuxi/backend/package/yuxi/knowledge/implementations/milvus.py"
  - "Yuxi/backend/package/yuxi/knowledge/chunking/ragflow_like/parsers/semantic.py"
  - "Yuxi/backend/package/yuxi/agents/toolkits/kbs/tools.py"
code_hash: ""
affects_path: []
trigger_keywords:
  - Milvus
  - PPR
  - Personalized PageRank
  - milvus.py
  - semantic chunking
  - KnowledgeBaseMiddleware
---

# Yuxi检索与知识图谱层

## 核心文件

- `milvus.py`（1255 行，检索核心实现）
- `semantic.py`（语义分块）
- `tools.py`（知识库 5 工具链）

## 混合检索 Pipeline

> 引用自分析：

```python
# 三种模式
search_mode: "vector" | "keyword" | "hybrid"

# Hybrid = Vector(COSINE) + BM25(内置) → WeightedRanker(0.7, 0.3)
```

## 图谱增强检索（PPR）

> 引用自分析：

```
Step 1: 并行搜索实体 + 三元组
Step 2: 构建种子权重
         entity命中=1.0, triple命中=0.8, base_chunks中的实体=0.3
Step 3: Personalized PageRank (damping=0.85, max_nodes=10000)
Step 4: RRF 融合图检索结果 (rrf_k=60)
```

## 语义分块机制

> 引用自分析：

```python
# 核心：按 Markdown AST 节点类型智能切分
# - heading_open → flush + 更新 title_stack
# - table_open → 表格整体作为一个 chunk
# - fence → 代码块保持完整
# - 超长 chunk → Embedding 相似度再切分
# 每个 chunk 带 title_path（标题链路）
```

## 5 工具链

| 工具 | 功能 | Token 效率 |
|------|------|-----------|
| `list_kbs` | 列出可用知识库 | 极低 |
| `get_mindmap` | 获取知识库思维导图 | 低 |
| `query_kb` | 语义检索（chunk 级） | 中 |
| `find_kb_document` | 文件内关键词/正则定位 | 低（只返回匹配行窗口） |
| `open_kb_document` | 按行窗口读取 | 可控（window_size 参数） |

## 双写一致性

> 引用自分析：

```python
# PostgreSQL（元数据+全文） + Milvus（向量+BM25）
# 双写事务保障：任意一路失败 → 回滚另一路
pg_task = chunk_repo.batch_upsert(...)
milvus_task = asyncio.to_thread(_insert_milvus_records)
results = await asyncio.gather(pg_task, milvus_task, return_exceptions=True)
```
