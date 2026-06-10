---
title: "Agent权限系统"
domain: ["agent_engineering"]
type: "concept"
tags: [权限系统, PermissionEngine, Bypass, Confirm, Agent安全]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "agentscope/src/agentscope/permission/"
affects_path: []
trigger_keywords:
  - Permission
  - PermissionEngine
  - PermissionMode
  - Bypass
  - Confirm
  - Agent权限
---

# Agent权限系统

## 核心概念

Agent 权限系统解决一个关键问题：**AI Agent 执行工具调用时，哪些操作需要人类确认，哪些可以自主执行？**

## AgentScope 的实现

> 引用自 README.md：
> "Fine-grained, configurable control over tools and resources."

### 三种权限模式

| 模式 | 说明 |
|------|------|
| **Bypass** | Agent 自主执行，无需确认 |
| **Confirm** | 暂停执行，等待人类确认 |
| **Deny** | 禁止执行 |

### 权限决策流程

```python
# 每个工具调用前：
decision = permission_engine.decide(tool_call, context)
match decision:
    case PermissionDecision.BYPASS:
        result = await tool.execute(params)
    case PermissionDecision.CONFIRM:
        # 发送 RequireUserConfirmEvent
        # 等待 UserConfirmResultEvent
        ...
    case PermissionDecision.DENY:
        result = ToolResult(state=DENIED, reason=...)
```

### 关键类

- `PermissionEngine`：权限决策引擎
- `PermissionContext`：包含当前会话/用户/Agent 的上下文
- `PermissionBehavior`：工具级的权限行为定义
- `PermissionMode`：全局权限模式

## 设计特征

1. **工具粒度**：每个工具可独立配置权限行为
2. **上下文感知**：根据用户身份、会话状态做决策
3. **可扩展**：自定义 PermissionEngine 实现自定义策略

## 对我们项目的启发

我们的知识库 Agent 在以下场景需要权限控制：

| 操作 | 建议权限 |
|------|---------|
| 知识检索（query） | Bypass（安全只读操作） |
| 知识摄入（ingest） | Confirm（会修改知识库） |
| 知识删除 | Confirm（不可逆操作） |
| 代码编译（compile） | Bypass（纯计算操作） |
| 外部 URL 抓取 | Confirm（涉及外部访问） |

关键启发：**Agent 的强大能力必须配合精细的权限控制，否则一次误操作可能破坏整个知识库**。
