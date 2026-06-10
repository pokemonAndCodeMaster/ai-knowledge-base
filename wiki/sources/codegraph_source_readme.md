---
title: "codegraph_source_readme"
domain: ["code_intelligence"]
type: "source"
tags: [CodeGraph, README, 项目介绍, MCP]
created: 2026-06-10
updated: 2026-06-10
status: active
original_path: "codegraph/README.md"
content_hash: ""
---

# CodeGraph README 来源记录

## 原文位置
`codegraph/README.md` (712 行)

## 核心内容摘要

### 项目定位
> "CodeGraph gives those agents a pre-indexed knowledge graph — symbol relationships, call graphs, and code structure."

### Benchmark 结果（7 个真实开源项目，Opus 4.8）

| Repo | Files | Cost Δ | Token Δ | Time Δ | Tool Calls Δ | Reads Δ |
|------|-------|--------|---------|--------|--------------|---------|
| Excalidraw | 643 | -45% | -75% | -25% | -87% | 9→0 |
| gin | 222 | -7% | -63% | -17% | -62% | 2→0 |
| VS Code | 10,446 | -36% | -76% | -33% | -81% | 9→0 |
| OkHttp | 601 | -10% | -18% | -37% | -64% | 3.5→2 |
| Django | 3,043 | -10% | -37% | 0% | -14% | 8.5→2 |
| Tokio | 1,538 | -12% | 0% | -29% | -59% | 7.5→2 |
| Alamofire | 177 | +7% | -60% | -13% | -38% | 4→3 |

平均：-16% cost, -47% tokens, -22% time, -58% tool calls

### 已验证语言
TypeScript, JavaScript, Python, Go, Rust, Java, C#, C, C++, PHP, Ruby, Swift, Kotlin, Dart, Svelte, Vue, Lua, Luau, Pascal, Liquid

## 分解出的知识卡片
- [[CodeGraph项目]] (entity)
- [[Tree-sitter AST解析引擎]] (concept)
- [[CodeGraph提取层]] ~ [[CodeGraph上下文层]] (code_module × 5)
