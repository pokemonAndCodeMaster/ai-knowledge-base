---
title: "CodeGraph项目"
domain: ["agent_engineering", "code_intelligence"]
type: "entity"
tags: [CodeGraph, Tree-sitter, MCP, 代码图谱, SQLite, FTS5, 语义搜索]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "codegraph/src/index.ts"
affects_path: []
trigger_keywords:
  - CodeGraph
  - codegraph
  - 代码图谱
  - code graph
  - code intelligence
  - Tree-sitter图谱
---

# CodeGraph项目

## 一句话定位

100% 本地的代码智能平台，用 Tree-sitter 解析任意语言的源码 AST，构建符号关系图谱并存入 SQLite，通过 MCP Server 为 AI Agent 提供语义级代码检索。

## 核心价值

> 引用自原文：
> "CodeGraph gives those agents a pre-indexed knowledge graph — symbol relationships, call graphs, and code structure. Agents query the graph instantly instead of scanning files."

**量化基准（7 个真实开源项目 × 4 runs/arm，Opus 4.8）：**
- 平均节省 16% 成本、47% Token、22% 时间、58% 工具调用
- VS Code (10k 文件): Tool calls 从 21 降到 4 (81%↓)，File Reads 从 9 降到 0

## 核心管线

```
files → ExtractionOrchestrator (tree-sitter AST 解析)
           → DB (SQLite: nodes / edges / files / FTS5)
               → ReferenceResolver (import解析 + 框架模式匹配)
                   → GraphQueryManager / GraphTraverser (BFS/DFS, 影响半径)
                       → ContextBuilder (Markdown/JSON 输出给 Agent)
                           → MCP Server (codegraph_explore 等 8 个工具)
```

## 技术栈

- **语言**: TypeScript
- **AST 解析**: Tree-sitter (WASM 运行时)
- **存储**: SQLite + FTS5 全文搜索
- **通信**: MCP (Model Context Protocol) over stdio
- **同步**: Native FSEvents / inotify / RDCW + 2s debounce
- **支持语言**: 20+ 语言 (TS, Python, Go, Rust, Java, C#, PHP, Ruby, C, C++, Swift, Kotlin, Dart, Svelte, Vue, Lua, Luau, Pascal 等)

## 关键设计哲学

1. **确定性提取 (Deterministic Extraction)**：所有知识来自 AST 解析，不使用 LLM 总结
2. **零配置**：语言支持自动从文件扩展名推断，无需手动配置
3. **100% 本地**：数据不出机器，无 API Key 依赖
4. **Adapt the tool, not the agent**：不试图改变 Agent 行为，而是把工具做得足够好

## 与其他项目的关系

- 与 [[graphify项目]] 同属代码知识图谱领域，但 codegraph 用 Tree-sitter 解析，graphify 用 SCIP 索引
- 为 [[知识库工业化升级_图索引检索系统]] 提供了"确定性代码图谱构建"的工业级参考
