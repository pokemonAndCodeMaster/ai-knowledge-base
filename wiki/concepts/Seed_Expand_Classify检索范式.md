---
title: "Seed-Expand-Classify 检索范式"
domain: ["knowledge_mgmt", "agent_engineering"]
type: "concept"
tags: [检索, 图遍历, BFS, Seed, 三阶段检索]
created: 2026-06-07
updated: 2026-06-07
sources: 0
status: active
related_code:
  - "scripts/query_graph.py"
affects_path: []
trigger_keywords:
  - Seed-Expand-Classify
  - 三阶段检索
  - BFS检索
  - 图遍历检索
  - 任务导向检索
  - 知识一网打尽
---

# Seed-Expand-Classify 检索范式

## 适用场景

给定一个具体**任务描述**（非单一概念查询），需要把知识库中所有相关知识点**全面收集**（领域知识、算法、规范、避坑等），而非返回 top-K 最相似的片段。

**与 top-K 向量检索的根本区别**：
- 向量检索：找"答案"（语义最相似的 K 个片段）
- Seed-Expand-Classify：找"弹药"（所有逻辑关联的知识，包括语义不相似但逻辑强关联的 pitfall/norm）

---

## 三阶段算法

### 阶段 1：Seed 发现（多维加权匹配）

输入：任务描述文本  
输出：3-5 个入口种子卡片

```python
权重分配：
  trigger_keywords 精确命中  → +3.0（每命中一个关键词）
  title 子串匹配             → +2.5
  affects_path 路径匹配      → +2.5（任务涉及特定代码路径时）
  related_code 路径匹配      → +2.5（任务涉及特定代码路径时）
  domain 匹配                → +1.5（明确指定领域时）
  tag 命中                   → +1.0（每命中一个）
  summary n-gram 重叠        → +0.3*n（最多 +1.5）
```

**中文匹配策略**：滑动窗口 n-gram（2-4 字）+ 英文词切分，零外部依赖。

### 阶段 2：图扩展（BFS 双向 2 跳）

输入：种子路径列表  
输出：所有 2 跳内的卡片 + 各自的跳数

```
从每个 seed 出发：
  hop=0：seed 本身
  hop=1：seed 的 outlinks 和 inlinks（双向）
  hop=2：hop-1 节点的 outlinks 和 inlinks（双向）

关键：inlinks（入站链接）同样参与扩展
  → 这是向量检索找不到的关联：
    比如 pitfall 卡片的 affects_path 指向某代码路径，
    但 pitfall 的内容和任务描述语义可能很远
    → 通过图中的 inlink 关系仍能被捕获
```

### 阶段 3：分类与优先级（按 type 分桶）

```
优先级规则（优先级决定 Agent 是否读全文）：

full_read（必须全文读取）：
  - type = pitfall | norm       ← 硬约束，必看全文
  - type = code_module           ← 代码关联，必看全文
  - 种子直接命中的 concept/synthesis

summary_only（只读预编译摘要）：
  - hop=1 的 concept/synthesis/module_doc
  - 无需读文件，直接用 .wiki_graph.json 中的 summary 字段

title_only（仅列标题）：
  - hop=2 的所有卡片
  - source / entity 类型卡片（除非 seed 直接命中）

交付格式：
  📋 领域知识: [concept 卡片]
  ⚠️ 避坑护栏: [pitfall 卡片全文]
  📐 操作规范: [norm 卡片全文]
  🔗 代码关联: [code_module 卡片]
  📚 参考来源: [source 标题列表]
```

---

## Token 消耗对比

| 检索方式 | 读文件数 | 估算 Token |
|---------|---------|-----------|
| 旧：逐文件遍历 | 10-15 全文 | ~50K |
| 新：三阶段检索（55 卡片） | 3-5 全文 + 3-5 摘要 | ~13K |
| 节省 | — | **约 75%** |

---

## 实现参考

- 完整 Python 实现：[[query_graph脚本]]
- 算法来源借鉴：gbrain（多维加权 Seed）+ Yuxi（分级读取工具链）
- 系统架构：[[知识库工业化升级_图索引检索系统]]
