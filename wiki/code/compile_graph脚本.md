---
title: "compile_graph脚本"
domain: ["knowledge_mgmt", "meta"]
type: "code_module"
tags: [图索引, 编译器, frontmatter解析, 邻接表]
created: 2026-06-07
updated: 2026-07-04
sources: 0
status: active
related_code:
  - "scripts/compile_graph.py"
code_hash: "sha256:18df9adae9592505"
affects_path: [".wiki_graph.json"]
trigger_keywords:
  - compile_graph
  - 编译知识图谱
  - 图索引编译
  - 构建图索引
  - 重建图谱
  - wiki_graph.json
---

# compile_graph脚本

## 职责（一句话）

解析 `wiki/` 下所有 `.md` 文件的 YAML frontmatter 和 `[[双链]]`，构建邻接表，输出 `.wiki_graph.json`。

## 运行方式

```bash
# 标准运行（项目根目录下）
python3 scripts/compile_graph.py

# 指定项目根目录
python3 scripts/compile_graph.py --project-root /path/to/project
```

## 关键函数与流程

```
main()
  └─ compile_graph(project_root)
       ├─ build_slug_to_path()     # 建 slug→path 映射（支持重名去重）
       ├─ for each .md file:
       │    ├─ parse_frontmatter() # 纯正则解析 YAML（零依赖）
       │    ├─ extract_wikilinks() # 正则提取 [[双链]]；忽略 ORIGINAL_START/END 原文快照区
       │    └─ extract_summary()   # 提取首段摘要（最多 200 字）
       ├─ 回填 inlinks             # 遍历所有 outlinks，反向写入 inlinks
       └─ 统计孤岛 / 断链
  └─ 输出 .wiki_graph.json
```

## 无损原文快照边界

NotebookLM 等来源卡可在 `<!-- ORIGINAL_START -->` 与 `<!-- ORIGINAL_END -->` 之间逐字符保存原始 Markdown。编译器不把该区域内属于上游文档的 `[[双链]]` 误认为本知识库的有效出链；来源卡自身的追踪链接应写在快照区外。

## 输出格式（.wiki_graph.json 节点结构）

```json
{
  "version": 1,
  "compiled_at": "2026-06-07T...",
  "stats": {
    "total_cards": 55,
    "total_links": 220,
    "orphan_count": 14,
    "orphan_cards": [...],
    "broken_link_count": 71,
    "broken_links": [{"from": "...", "target": "..."}]
  },
  "nodes": {
    "wiki/concepts/xxx.md": {
      "title": "...", "slug": "xxx",
      "domain": [...], "type": "...",
      "tags": [...], "trigger_keywords": [...],
      "affects_path": [...], "related_code": [...],
      "status": "active", "summary": "...",
      "outlinks": [...], "inlinks": [...]
    }
  }
}
```

## 核心设计决策

1. **纯正则解析 YAML frontmatter**：不依赖 PyYAML，处理 string/list/int/bool 四种类型，足够覆盖本项目 schema
2. **slug 重名策略**：同名文件（不同目录）保留路径较短者，其余卡片需在 `[[双链]]` 中用完整路径消歧
3. **双向链接回填**：先收集所有 outlinks，再遍历一遍回填 inlinks，确保图是双向可遍历的
4. **code_module 特殊处理**：自动计算 `related_code` 中各文件的 SHA256 hash，写入节点的 `code_hashes` 字段

## 与其他脚本的关系

- 是 [[query_graph脚本]] 和 [[check_staleness脚本]] 的**前置依赖**
- 产物 `.wiki_graph.json` 是整个系统的核心数据
- 应在每次 `[ingest]` 后运行（见 [[知识图谱编译与检索操作规范]]）
