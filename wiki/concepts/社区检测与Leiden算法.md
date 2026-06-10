---
title: "社区检测与Leiden算法"
domain: ["code_intelligence", "graph_algorithm"]
type: "concept"
tags: [社区检测, Leiden算法, 图聚类, 模块发现, NetworkX]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "graphify/graphify/cluster.py"
affects_path: []
trigger_keywords:
  - 社区检测
  - community detection
  - Leiden
  - 图聚类
  - graph clustering
  - modularity
---

# 社区检测与Leiden算法

## 核心概念

社区检测（Community Detection）是图分析中发现自然聚类结构的算法族。在代码知识图谱中，它能自动发现**代码模块边界**——哪些类/函数/文件天然地紧密关联。

## Leiden算法

> 引用自原文（how-it-works.md）：
> "Communities are found using the Leiden algorithm — a graph-clustering method that groups nodes by edge density. Nodes with many connections between them end up in the same community."
> "**No embeddings needed.** The semantic similarity edges that Claude extracts (`semantically_similar_to`) are already in the graph, so they influence community shape directly."

### 关键特征

1. **基于边密度**：内部边密度高的节点集合被划为同一社区
2. **不需要嵌入**：直接在图结构上运行，语义相似性已经通过边编码
3. **分辨率可调**：`--resolution` 参数控制社区粒度，值越大社区越小越细
4. **Hub 排除**：`--exclude-hubs 99` 可以排除 p99 度数的超级 hub 节点

## 在 Graphify 中的实现

> 引用自原文（ARCHITECTURE.md）：
> `cluster.py` | `cluster(G)` | graph → graph with `community` attr on each node

```python
# 使用方式
graphify cluster-only ./my-project --resolution 1.5 --exclude-hubs 99
```

## 输出物

分析报告 (GRAPH_REPORT.md) 中的关键产出：

> 引用自原文（README.md）：
> - **God nodes** — the most-connected concepts in your project
> - **Surprising connections** — links between things that live in different files or modules
> - **Suggested questions** — 4–5 questions the graph is uniquely positioned to answer

## 对知识库的启发

社区检测可以用于我们知识库的**卡片自动分组和关联发现**：
1. 以知识卡片为节点、`[[双链]]` 为边构建图
2. 运行 Leiden 算法发现卡片自然聚类
3. 每个社区可以自动生成"领域概览"卡片
4. 跨社区的边就是"意外连接"——可能揭示被忽视的知识关联
