---
title: "query_graph脚本"
domain: ["knowledge_mgmt", "meta"]
type: "code_module"
tags: [检索, 图遍历, BFS, query, Seed]
created: 2026-06-07
updated: 2026-06-07
sources: 0
status: active
related_code:
  - "scripts/query_graph.py"
code_hash: "sha256:bbbd954ba9714207"
affects_path: []
trigger_keywords:
  - query_graph
  - 检索脚本
  - BFS检索
  - 图查询
  - 知识检索实现
---

# query_graph脚本

## 职责（一句话）

基于 `.wiki_graph.json` 编译产物，执行 [[Seed-Expand-Classify检索范式]]，给定任务描述，返回分级排序的相关卡片清单（JSON）。

## 运行方式

```bash
# 基础用法
python3 scripts/query_graph.py "设计一个多Agent协作系统"

# 涉及特定代码路径时（大幅提升召回率）
python3 scripts/query_graph.py "重构检索脚本" --paths "scripts/"

# 指定领域（精准过滤）
python3 scripts/query_graph.py "知识检索方案" --domains "knowledge_mgmt,agent_engineering"

# 调参
python3 scripts/query_graph.py "..." --max-hops 3 --top-seeds 8
```

## 关键函数与流程

```
main()
  ├─ 加载 .wiki_graph.json
  ├─ find_seeds(task, nodes, opts, top_k=5)
  │    ├─ _tokenize_simple()       # n-gram + 英文词切分，零依赖
  │    └─ 多维加权打分（见范式卡片）
  ├─ expand_from_seeds(seeds, nodes, max_hops=2)
  │    └─ BFS 双向扩展（outlinks + inlinks）
  └─ classify_results()
       ├─ assign_priority()        # pitfall/norm/code_module → full_read
       └─ 按优先级+跳数排序输出
```

## 输出格式

```json
{
  "task": "...",
  "graph_compiled_at": "...",
  "total_graph_cards": 55,
  "seeds": [{"path": "...", "title": "...", "score": 2.5, "reason": "tag:Agent"}],
  "total_retrieved": 21,
  "classified": {
    "concept": [...],
    "pitfall": [...],
    "norm": [...]
  },
  "suggested_read_order": [
    {"path": "...", "title": "...", "type": "pitfall", "priority": "full_read", "hop_count": 1}
  ],
  "read_stats": {"full_read": 3, "summary_only": 3, "title_only": 15}
}
```

## Agent 使用方式

```
1. 运行脚本，得到 JSON
2. 读 suggested_read_order：
   - priority=full_read → view_file() 读全文
   - priority=summary_only → 直接使用 JSON 中的 summary 字段，不读文件
   - priority=title_only → 仅展示标题，不读文件
3. pitfall/norm 卡片的内容在交付时必须显式引用
```

## 典型召回效果（55 张卡片）

| 查询 | 命中 | full_read | summary | title |
|------|------|-----------|---------|-------|
| "设计多Agent系统" | 21 | 3 | 3 | 15 |
| "高效学习新技术" | 22 | 2 | 10 | 10 |

## 关键依赖

- 前置：[[compile_graph脚本]]（必须先编译）
- 范式：[[Seed-Expand-Classify检索范式]]
- 系统规范：[[知识图谱编译与检索操作规范]]
