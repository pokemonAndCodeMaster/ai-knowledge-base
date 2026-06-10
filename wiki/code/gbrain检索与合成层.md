---
title: "gbrain检索与合成层"
domain: ["knowledge_management"]
type: "code_module"
tags: [gbrain, hybrid search, RRF, BrainEngine, think, query]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "gbrain/src/core/search/hybrid.ts"
  - "gbrain/src/core/"
code_hash: ""
affects_path: []
trigger_keywords:
  - hybridSearch
  - BrainEngine
  - postFusionStages
  - weightsForIntent
  - aliasHop
---

# gbrain检索与合成层

## 核心文件

`gbrain/src/core/search/hybrid.ts`（1871 行，混合检索核心）

## 检索 Pipeline

> 引用自分析：

```
Query
  │
  ▼
Intent Classification → weightsForIntent() → 动态调整权重
  │
  ├──→ Vector Search (HNSW, pgvector)
  │       embedding: ZeroEntropy / OpenAI / Voyage
  │       max-pool：每页取最强 chunk
  │
  ├──→ BM25 Keyword Search
  │
  ▼
RRF Fusion (score = Σ 1/(60 + rank))
  │
  ▼
Post-Fusion Stages（6 阶段）：
  1. Backlink Boost     (被引用数)
  2. Salience Boost     (显著性)
  3. Recency Boost      (新鲜度)
  4. Title-Phrase Boost  (标题匹配)
  5. Graph Signals      (图邻居)
  6. Alias-Resolved     (别名标准化)
  │
  ▼
Alias Hop → Reranker → Dedup → Token Budget 截断
```

## BrainEngine Interface

~47 个操作，两个实现（PGLiteEngine / PostgresEngine）共享同一接口：

- 搜索：`hybridSearch`, `vectorSearch`, `keywordSearch`
- 知识：`getPage`, `createPage`, `updatePage`, `deletePage`
- 图谱：`getLinks`, `getBacklinks`, `getNeighbors`
- 提取：`extractAtoms`, `extractLinks`
- 嵌入：`embedPage`, `embedChunks`
- 评分：`computeBrainScore`

## 合成层

`gbrain think` 命令：检索 → 合成答案 → Gap Analysis

- 检索相关页面
- 合成连贯答案
- 标注"头脑不知道什么"（Gap Analysis）
- 防止用户误信过时信息
