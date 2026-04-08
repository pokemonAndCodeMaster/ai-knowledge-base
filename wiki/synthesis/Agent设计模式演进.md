---
title: Agent 设计模式演进
tags: [综合分析, AI, Agent, 架构]
created: 2026-04-07
updated: 2026-04-07
sources: 1
status: active
---
# Agent 设计模式演进

本文综合分析了 2026 年智能体设计模式从经典到前沿的演变，以及支撑这些模式的工程架构。

## 经典基石模式 (Andrew Ng 体系)
早期的 Agent 设计主要依赖于模型本身的认知能力，通过多次 Prompt 交互形成闭环：
1. **Reflection (反思模式)**：生成初稿 -> Critic 挑刺 -> 修正。
2. **Tool Use (工具调用)**：赋予物理接口，杜绝幻觉。
3. **Planning (规划模式)**：分解复杂目标为 DAG 子任务。
4. **Multi-Agent Collaboration (多体协作)**：解耦系统逻辑。

## 2026 前沿进阶模式
随着 [[Agent_Engineering]] 的发展，模式开始引入强力的外部约束：
- **ReAct (Reason + Act)**：强制 `Thought -> Action -> Observation` 循环。
- **Dynamic Routing (动态路由)**：轻量级意图识别 + 重型专精 Agent。
- **Human-in-the-Loop (HITL)**：在执行高危操作时，挂起线程请求人工干预。

## 架构的底层支撑：Harness Engineering
这些高级模式的落地，离不开 [[Harness_Engineering]]（脚经过脚手架工程）的支撑。为了防止单个 Agent "既当裁判又当运动员"，像 Anthropic 的三智能体护栏模式或 Stripe 的 Minions 架构，都在 Harness 层面实现了物理隔离和严格的验证闭环（Verification Loops）。

## 关联实践
- [[Cognitive_Gearing]]：通过切换系统提示词改变 Agent 重点，属于一种微观的 Multi-Agent Collaboration 实践。