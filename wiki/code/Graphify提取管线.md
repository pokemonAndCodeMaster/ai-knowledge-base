---
title: "Graphify提取管线"
domain: ["code_intelligence"]
type: "code_module"
tags: [Graphify, extract, detect, build, cluster, analyze]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "graphify/graphify/extract.py"
  - "graphify/graphify/detect.py"
  - "graphify/graphify/build.py"
  - "graphify/graphify/cluster.py"
  - "graphify/graphify/analyze.py"
  - "graphify/graphify/report.py"
  - "graphify/graphify/export.py"
code_hash: ""
affects_path: []
trigger_keywords:
  - graphify extract
  - graphify detect
  - graphify build
  - graphify cluster
  - graphify analyze
---

# Graphify提取管线 (Extraction Pipeline)

## 管线概览

> 引用自原文（ARCHITECTURE.md）：
> "Each stage is a single function in its own module. They communicate through plain Python dicts and NetworkX graphs - no shared state, no side effects outside `graphify-out/`."

```
detect() → extract() → build_graph() → cluster() → analyze() → report() → export()
```

## 各模块职责

| 模块 | 入口函数 | 职责 |
|------|---------|------|
| `detect.py` | `collect_files(root)` | 目录扫描，过滤出需要处理的文件列表 |
| `extract.py` | `extract(path)` | 对单个文件执行 AST 或语义提取，返回 `{nodes, edges}` |
| `build.py` | `build_graph(extractions)` | 将所有提取结果合并为 NetworkX 图 |
| `cluster.py` | `cluster(G)` | Leiden 社区检测，给节点添加 `community` 属性 |
| `analyze.py` | `analyze(G)` | 图分析：God 节点、意外连接、推荐问题 |
| `report.py` | `render_report(G, analysis)` | 生成 GRAPH_REPORT.md |
| `export.py` | `export(G, out_dir, ...)` | 导出 Obsidian vault / graph.json / HTML / SVG |
| `cache.py` | `check_semantic_cache / save_semantic_cache` | SHA256 缓存管理 |
| `validate.py` | `validate_extraction(data)` | 提取结果 schema 校验 |

## 特殊提取器

- **callflow_html.py**：Mermaid 架构/调用流 HTML 生成
- **ingest.py**：URL 内容获取与存储
- **serve.py**：MCP Server（stdio/HTTP）
- **watch.py**：文件变更监听，写 flag 文件触发重建
- **benchmark.py**：Token 使用量基准测试

## 并行化策略

> 引用自原文（how-it-works.md）：
> "Code files are extracted in parallel using `ProcessPoolExecutor` — bypasses Python's GIL for genuine multiprocessing."

- 代码：`ProcessPoolExecutor` 多进程并行 AST 提取
- 文档：Claude 子 Agent 并行语义提取
- 控制参数：`--max-workers` / `GRAPHIFY_MAX_WORKERS`

## 安全机制

> 引用自原文（ARCHITECTURE.md）：
> "All external input passes through `graphify/security.py` before use"

- URL → `validate_url()`（只允许 http/https）
- 文件 → `validate_graph_path()`（必须在 `graphify-out/` 内）
- 标签 → `sanitize_label()`（去控制字符，限 256 字符，HTML 转义）
