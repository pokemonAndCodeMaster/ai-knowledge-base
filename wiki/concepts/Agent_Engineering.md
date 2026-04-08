---
title: Agent Engineering
tags: [概念, AI, Agent]
created: 2026-04-07
updated: 2026-04-07
sources: 1
status: active
---
# Agent Engineering (智能体工程)

Agent Engineering 是构建自主 AI 系统的工程学科。与早期的 Prompt Engineering 不同，它更强调整体的架构设计、工作流约束和状态管理。

## 核心实践
现代 Agent 摒弃“自由发挥”，采用高约束力的工作流（Skills）来保证工业级输出：
- **验证优先 (Verification-First)**：强制 Agent 在声明完成前必须给出测试通过的物理证据（如 [[Agent-Skills]] 的实践）。
- **拦截器工作流**：在执行前强制激活特定的设计模式（如 [[test-driven-development]] 或 [[brainstorming]]）。

## 关联模式
- [[Harness_Engineering]]：提供物理约束的“身体”。
- 经典设计模式：Reflection（反思）、Tool Use（工具调用）、Planning（规划）、Multi-Agent Collaboration（多体协作）。
- 前沿设计模式：ReAct、Dynamic Routing、Human-in-the-Loop (HITL)。