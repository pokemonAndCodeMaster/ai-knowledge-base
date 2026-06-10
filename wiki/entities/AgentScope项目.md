---
title: "AgentScope项目"
domain: ["agent_engineering"]
type: "entity"
tags: [AgentScope, 多Agent, Agent框架, 阿里巴巴, FastAPI, 工具系统, 权限系统]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "agentscope/src/agentscope/"
affects_path: []
trigger_keywords:
  - AgentScope
  - agentscope
  - Agent框架
  - multi-agent platform
  - Agent Team
  - PermissionEngine
---

# AgentScope项目

## 一句话定位

阿里巴巴出品的生产级 Agent 框架（Python），核心设计哲学是"利用 LLM 的推理和工具使用能力，而非用严格提示词和编排约束模型"。

## 核心架构（2.0）

> 引用自 README.md：
> "We design for increasingly agentic LLMs. Our approach leverages the models' reasoning and tool use abilities rather than constraining them with strict prompts and opinionated orchestrations."

### 五大核心系统

| 系统 | 说明 |
|------|------|
| **Event System** | 统一事件总线，连接前端 + human-in-the-loop |
| **Permission System** | 细粒度、可配置的工具和资源访问控制 |
| **Multi-tenancy Service** | 多租户多会话隔离的生产级服务 |
| **Workspace / Sandbox** | 工具/代码在隔离环境运行（Local / Docker / E2B） |
| **Middleware System** | 可组合 Hook，自定义 Agent 推理-行动循环 |

### 代码模块结构（215 文件）

```
agentscope/src/agentscope/
├── agent/        → Agent 核心类 + ReAct 配置
├── app/          → FastAPI 多租户服务
│   ├── _router/  → REST API 路由（agent/chat/session/schedule/...）
│   ├── _service/ → 业务逻辑层
│   └── _manager/ → 后台任务/调度/唤醒管理器
├── tool/         → 工具系统（Toolkit/ToolBase/内置工具）
├── permission/   → 权限引擎（PermissionEngine + Mode + Behavior）
├── event/        → 事件系统（30+ 事件类型）
├── middleware/   → 中间件系统
├── model/        → 模型适配层（多供应商）
├── message/      → 消息类型（Msg/Block/ToolCall/...）
├── credential/   → 凭证管理
├── workspace/    → 沙箱环境
├── state/        → Agent 状态管理
├── skill/        → 技能系统
├── mcp/          → MCP 协议支持
└── formatter/    → 格式化器
```

## 技术栈

- **语言**: Python 3.11+
- **Web 框架**: FastAPI
- **模型**: DashScope / OpenAI / Anthropic 等
- **沙箱**: Local / Docker / E2B
- **通信**: Event-driven + SSE 流式

## 关键设计特征

1. **Event-driven 架构**：30+ 事件类型，`reply_stream()` 异步生成器驱动
2. **Permission-first**：每个工具调用前经过 `PermissionEngine` 决策（Bypass/Confirm/Deny）
3. **Agent Team**：Leader Agent 可以 spawn Worker Agent 并协调
4. **Background Task Offloading**：长时间运行的工具移到后台，结果返回时唤醒 Agent
5. **Middleware 可组合**：类似 Express/Koa 的中间件栈

## 对我们项目的启发

AgentScope 的设计特别适合作为我们 Agent 系统搭建的参考：
- **Permission System**：我们的知识库 Agent 需要区分读/写权限
- **Event System**：为未来的前端交互提供基础
- **Agent Team**：多 Agent 协作的参考实现
- **Middleware**：可插拔能力栈的设计模式

## 论文引用

- AgentScope 2.0: Production-ready agent framework
- ArXiv: 2402.14034, 2508.16279
