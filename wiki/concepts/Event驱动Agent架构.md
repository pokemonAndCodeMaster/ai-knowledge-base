---
title: "Event驱动Agent架构"
domain: ["agent_engineering"]
type: "concept"
tags: [Event驱动, 事件总线, Agent架构, 流式, SSE]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "agentscope/src/agentscope/event/"
affects_path: []
trigger_keywords:
  - Event System
  - EventType
  - reply_stream
  - 事件驱动
  - Agent事件
---

# Event驱动Agent架构

## 核心概念

Event-driven（事件驱动）架构是 [[AgentScope项目]] 的核心设计模式。Agent 的每个动作（思考、调用工具、生成文本）都会产生事件，通过统一事件总线分发给前端 UI、日志系统、监控等消费者。

## AgentScope 的 30+ 事件类型

| 事件组 | 事件类型 | 说明 |
|--------|---------|------|
| **Reply** | ReplyStart / ReplyEnd | Agent 回复的生命周期 |
| **Model** | ModelCallStart / ModelCallEnd | LLM 调用的生命周期 |
| **Text** | TextBlockStart / Delta / End | 文本块的流式生成 |
| **Thinking** | ThinkingBlockStart / Delta / End | 思考过程的流式输出 |
| **ToolCall** | ToolCallStart / Delta / End | 工具调用的生命周期 |
| **ToolResult** | ToolResultStart / Data / Text / End | 工具结果的流式返回 |
| **Permission** | RequireUserConfirm / UserConfirmResult | 权限确认事件 |
| **External** | RequireExternalExecution / ExternalExecutionResult | 外部执行事件 |
| **Data** | DataBlockStart / Delta / End | 数据块传输 |
| **Control** | ExceedMaxIters | 超出最大迭代次数 |

## 流式架构

```python
async for evt in agent.reply_stream(UserMsg("Tony", "Hi!")):
    match evt.type:
        case EventType.TEXT_BLOCK_DELTA:
            # 实时渲染文本
        case EventType.TOOL_CALL_START:
            # 显示工具调用
        case EventType.REQUIRE_USER_CONFIRM:
            # 弹出确认对话框
```

## 设计优势

1. **解耦**：Agent 核心逻辑不关心谁消费事件
2. **流式**：所有输出都是增量的，用户体验好
3. **可观测**：每个事件都是监控和调试的数据点
4. **可扩展**：新增消费者不修改 Agent 代码
5. **Human-in-the-loop**：权限确认事件自然支持人类介入

## 对我们项目的启发

Event-driven 模式可以应用于知识库的以下场景：
1. **知识摄入进度**：实时展示每个文档的处理进度
2. **检索调试**：实时展示检索的每个阶段（分词→BM25→图扩展→排序）
3. **Agent 监控**：追踪 Agent 读取了哪些知识卡片、做了什么决策
