---
title: "CodeGraph图遍历层"
domain: ["code_intelligence"]
type: "code_module"
tags: [CodeGraph, 图遍历, BFS, DFS, 影响半径, 调用链]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "codegraph/src/graph/index.ts"
  - "codegraph/src/graph/traverser.ts"
code_hash: ""
affects_path: []
trigger_keywords:
  - GraphTraverser
  - GraphQueryManager
  - BFS
  - DFS
  - impact radius
  - callers
  - callees
---

# CodeGraph图遍历层 (Graph Layer)

## 职责

在 [[CodeGraph存储层]] 之上提供图算法能力，支持调用链查询、影响半径分析、路径查找等高级功能。

## 核心组件

- **GraphTraverser** (`traverser.ts`)：图遍历引擎
  - BFS / DFS 遍历
  - **Impact Radius**：从一个节点出发，沿 calls/extends/implements 边扩展 N 层
  - **Path Finding**：在图中找到两个符号之间的连通路径
- **GraphQueryManager** (`index.ts`)：高级查询封装
  - `getCallers(nodeId)`：获取所有调用者
  - `getCallees(nodeId)`：获取所有被调用者
  - `getImpactRadius(nodeId, depth)`：获取变更影响范围

## MCP 工具映射

| 图查询 | MCP 工具 | 用途 |
|--------|---------|------|
| 调用者查询 | `codegraph_callers` | "谁调用了这个函数？" |
| 被调用者查询 | `codegraph_callees` | "这个函数调用了什么？" |
| 影响半径 | `codegraph_impact` | "改这个类会影响什么？" |
| Flow 追踪 | `codegraph_explore` (via buildFlowFromNamedSymbols) | "A 怎么调用到 B？" |

## 与其他层的关系

- 上游：查询 [[CodeGraph存储层]] 的 nodes 和 edges
- 下游：被 [[CodeGraph上下文层]] 和 MCP 工具调用
