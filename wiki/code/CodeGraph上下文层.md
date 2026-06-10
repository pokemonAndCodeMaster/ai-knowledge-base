---
title: "CodeGraph上下文层"
domain: ["code_intelligence", "agent_engineering"]
type: "code_module"
tags: [CodeGraph, ContextBuilder, MCP, explore, 代码上下文]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "codegraph/src/context/index.ts"
  - "codegraph/src/mcp/tools.ts"
  - "codegraph/src/mcp/server-instructions.ts"
  - "codegraph/src/mcp/transport.ts"
code_hash: ""
affects_path: []
trigger_keywords:
  - ContextBuilder
  - codegraph_explore
  - MCP server
  - server instructions
  - buildFlowFromNamedSymbols
---

# CodeGraph上下文层 (Context + MCP Layer)

## 职责

将 [[CodeGraph图遍历层]] 的查询结果格式化为 Agent 可理解的 Markdown/JSON 上下文，并通过 MCP 协议暴露给 AI Agent。

## 核心组件

### 上下文构建
- **ContextBuilder** (`context/index.ts`)：将子图转为 Markdown 格式
- **findRelevantContext**：混合搜索（FTS5 + 图遍历），核心的上下文聚合函数

### MCP 服务
- **MCPServer** (`mcp/server.ts`)：MCP 服务器主体
- **tools.ts**：所有 MCP 工具的实现
  - `handleExplore`：最核心的工具，包含 `buildFlowFromNamedSymbols`、自适应骨架化等
  - Explore 预算计算：`getExploreBudget`、`getExploreOutputBudget`
- **server-instructions.ts**：MCP `initialize` 响应中返回的 Agent 指导文本（唯一真相源）
- **transport.ts**：MCP 传输层

## MCP 工具清单

| 工具 | 角色 | 说明 |
|------|------|------|
| `codegraph_explore` | **PRIMARY** | Agent 最可靠调用的工具，接受符号名列表，返回相关源码 + Flow 追踪 |
| `codegraph_node` | SECONDARY | 深度查看单个符号的完整源码 + caller/callee trail |
| `codegraph_search` | 辅助 | 按名称搜索符号（FTS5 BM25） |
| `codegraph_callers` | 辅助 | 查询某符号的调用者 |
| `codegraph_callees` | 辅助 | 查询某符号的被调用者 |
| `codegraph_impact` | 辅助 | 变更影响分析 |
| `codegraph_files` | 辅助 | 列出已索引文件 |
| `codegraph_status` | 辅助 | 索引状态查看 |

## codegraph_explore 的内部流程

1. 解析 Agent 给的符号名列表
2. FTS5 搜索 + 精确名称匹配
3. 从命中符号出发做图遍历（traversalDepth=3, maxNodes=80）
4. `buildFlowFromNamedSymbols`：在命中的符号间构建 Flow 路径
5. [[Explore自适应骨架化]]：多态兄弟文件只渲染签名
6. 格式化为 Markdown 输出（文件分组 + Flow 部分置顶）

## 关键设计原则

> 引用自原文：
> "**Adapt the tool to the agent — don't try to change the agent.** The lever that decides whether a retrieval change lands."

Agent 的工具选择行为几乎无法通过提示词改变。正确的做法是把 `codegraph_explore`（Agent 已经会选择的工具）做到足够好，而不是创建新工具期望 Agent 去选。

## 与其他层的关系

- 上游：调用 [[CodeGraph图遍历层]] 和 [[CodeGraph存储层]] 的查询能力
- 下游：通过 MCP 协议直接服务 Claude / Cursor / Codex 等 Agent
