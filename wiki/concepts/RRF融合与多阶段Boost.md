---
title: "RRF融合与多阶段Boost"
domain: ["knowledge_management", "information_retrieval"]
type: "concept"
tags: [RRF, 混合检索, Reciprocal Rank Fusion, Boost, 检索排序]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "gbrain/src/core/search/hybrid.ts"
affects_path: []
trigger_keywords:
  - RRF
  - Reciprocal Rank Fusion
  - hybrid search
  - 混合检索
  - post-fusion
  - boost
---

# RRF融合与多阶段Boost

## 核心概念

RRF（Reciprocal Rank Fusion）是将多个检索通道的排序结果融合为统一排序的标准算法。公式：

```
score(d) = Σ 1/(k + rank_in_list_i)
```

其中 `k` 通常取 60，用于平滑排名差异。

## gbrain 的工业级实现

> 引用自分析（`hybrid.ts` 1871行核心）：
> 实测效果：**P@5 49.1%, R@5 97.9%**，相比 graph-disabled 变体 **+31.4 P@5**

### 检索通道

```
Query → Intent Classification → weightsForIntent() → 动态调整权重
  ├── Vector Search (HNSW, pgvector)
  └── BM25 Keyword Search
      → RRF Fusion
```

### 6 阶段 Post-Fusion Boost

> 引用自分析：

| 阶段 | 公式 | 说明 |
|------|------|------|
| 1. Backlink Boost | `score *= 1 + 0.05 * log(1 + count)` | 被引用越多越重要 |
| 2. Salience Boost | `score *= 1 + k * log(1 + score)` | 显著性加成 |
| 3. Recency Boost | `score *= 1 + α * halflife/(halflife+days)` | 新鲜度加成 |
| 4. Title-Phrase Boost | `1.25x` | query 是 title 子串 |
| 5. Graph Signals | 图谱邻居 hub 加分 | 图结构信号 |
| 6. Alias-Resolved | `1.05x` | 别名的 canonical 页 |

### Floor Ratio Gate（防翻盘机制）

> 引用自分析：
> "防止弱相关页面通过多重 boost 翻盘强相关页面"

```typescript
const floorThreshold = topScore * floorRatio;
// 所有 metadata boost 阶段都检查：if (r.score < floorThreshold) continue
```

## Yuxi 的实现

> 引用自分析：

```python
# Milvus 内置 hybrid_search
hybrid_search(
    reqs=[vector_request, bm25_request],
    rerank=WeightedRanker(vector_weight=0.7, bm25_weight=0.3),
    limit=recall_top_k,
)
```

Yuxi 在 RRF 基础上增加 PPR（Personalized PageRank）图谱增强。

## 对知识库的启发

我们的 [[知识库工业化升级_图索引检索系统]] 已实现了 BM25 + 图扩展 + 关键词匹配的融合检索。RRF 融合 + Post-Fusion Boost 可以作为下一步的检索质量提升方向。
