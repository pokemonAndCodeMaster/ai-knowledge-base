---
title: "Graphify项目"
domain: ["agent_engineering", "code_intelligence"]
type: "entity"
tags: [Graphify, 知识图谱, 社区检测, Tree-sitter, MCP, Claude, NetworkX]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "graphify/graphify/"
affects_path: []
trigger_keywords:
  - Graphify
  - graphify
  - 代码图谱
  - knowledge graph
  - community detection
---

# Graphify项目

## 一句话定位

多模态知识图谱构建工具，将代码（AST）+ 文档（LLM 语义提取）+ 图片 + 视频统一构建为 NetworkX 知识图谱，通过 MCP Server / CLI 为 AI Agent 提供代码理解能力。

## 核心价值

> 引用自原文（README.md）：
> "Type `/graphify` in your AI coding assistant and it maps your entire project — code, docs, PDFs, images, videos — into a knowledge graph you can query instead of grepping through files."

> 引用自原文（how-it-works.md）：
> "On a mixed corpus (Karpathy repos + 5 papers + 4 images, 52 files): **71.5x fewer tokens per query** vs reading the raw files directly."

## 三阶段管线

> 引用自原文（ARCHITECTURE.md）：
> ```
> detect() → extract() → build_graph() → cluster() → analyze() → report() → export()
> ```

**Pass 1 — 代码结构（免费，无 API 调用）：** Tree-sitter 解析代码 AST，提取类、函数、import、调用图。25+ 语言支持。

**Pass 2 — 视频/音频（本地，无 API 调用）：** faster-whisper 本地转录。

**Pass 3 — 文档/PDF/图片（LLM 子 Agent，消耗 token）：** Claude/Gemini/OpenAI/Ollama 并行语义提取。

## 输出物

```
graphify-out/
├── graph.html       # 交互式可视化（点击节点、过滤、搜索）
├── GRAPH_REPORT.md  # 分析报告（God节点、意外连接、推荐问题）
└── graph.json       # 完整图谱（NetworkX node-link 格式）
```

## 技术栈

- **语言**: Python
- **AST 解析**: Tree-sitter (25+ 语言)
- **图引擎**: NetworkX
- **社区检测**: Leiden 算法
- **通信**: MCP Server (stdio + HTTP)
- **语义提取**: Claude / Gemini / OpenAI / Ollama / Bedrock / Azure

## 关键设计特征

1. **混合提取**：代码用确定性 AST，文档用 LLM 语义，视频用本地转录
2. **置信度标记**：每条边标记 EXTRACTED / INFERRED / AMBIGUOUS
3. **社区检测**：Leiden 算法自动发现代码模块边界
4. **SHA256 缓存**：增量更新，跳过未变更文件
5. **多 Agent 平台支持**：20+ 个 IDE/CLI Agent 平台

## 与其他项目的关系

- 与 [[CodeGraph项目]] 同属代码知识图谱领域，区别在于 graphify 是混合模态（代码 + 文档 + 多媒体），而 CodeGraph 专注纯代码
- 为我们的知识库系统提供了"混合提取"、"置信度标记"、"社区检测"的参考
