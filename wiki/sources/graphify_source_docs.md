---
title: "graphify_source_docs"
domain: ["code_intelligence"]
type: "source"
tags: [Graphify, README, ARCHITECTURE, how-it-works]
created: 2026-06-10
updated: 2026-06-10
status: active
original_path: "graphify/README.md + graphify/ARCHITECTURE.md + graphify/docs/how-it-works.md"
content_hash: ""
---

# Graphify 文档来源记录

## 原文位置
- `graphify/README.md` (694 行)
- `graphify/ARCHITECTURE.md` (86 行)
- `graphify/docs/how-it-works.md` (99 行)

## 核心内容提炼

### README.md
- 项目定位：多模态知识图谱构建工具
- 20+ Agent 平台支持
- Token 节省基准：52 文件混合语料 → 71.5x 压缩
- 完整 CLI 命令参考（80+ 子命令）
- 隐私保护：代码本地处理，无遥测

### ARCHITECTURE.md
- 7 步管线：detect → extract → build_graph → cluster → analyze → report → export
- 提取数据 schema：nodes[id, label, source_file, source_location] + edges[source, target, relation, confidence]
- 置信度三级标记：EXTRACTED / INFERRED / AMBIGUOUS
- 安全层：所有外部输入通过 security.py 校验

### how-it-works.md
- 三阶段提取：代码(AST) → 视频(whisper) → 文档(LLM)
- 社区检测：Leiden 算法，不需要嵌入
- SHA256 缓存：增量更新
- 并行化：ProcessPoolExecutor + Claude 子 Agent

## 分解出的知识卡片
- [[Graphify项目]] (entity)
- [[社区检测与Leiden算法]] (concept)
- [[混合模态知识提取]] (concept)
- [[Graphify提取管线]] (code_module)
