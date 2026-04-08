---
title: Agent Harness Engineering（智能体约束工程）
tags: [核心概念, agent-engineering, harness, 工程学科, 2026新兴领域]
created: 2026-04-08
updated: 2026-04-08
sources: 6
status: active
---

# Agent Harness Engineering（智能体约束工程）

**关联节点**：[[Harness Stack 分层架构]] | [[前馈与反馈控制]] | [[渐进式上下文披露]] | [[Agent 工作流五大模式]] | [[awesome_agent_harness]] | [[martin_fowler_harness_engineering]]

---

## 定义

**Agent Harness** = LLM coding agent 的外围基础设施，即除模型本身以外的一切：会话管理、上下文交付、工具设计、架构强制、故障恢复和人类监督。

**公式**：`Agent = Model + Harness`

> "Harness Engineering 是一门设计环境、指定意图，并构建能让 agents 可靠工作的反馈循环的学科。" —— OpenAI（2026）

---

## 为什么 Harness 比模型更重要？

Anthropic 的 Claude Code 团队在实践中发现：
- 更少、更有表达能力的工具 > 大量狭窄工具
- 渐进式披露上下文 > 一次性加载所有内容
- Harness 的设计决定了产出是否有用

> "设计 agent 的动作空间既是艺术，也是科学。" —— Thariq（Claude Code Team Lead）

---

## 两大奠基文献

1. **OpenAI Harness Engineering 博客**（2026）：1M+ 行零人工代码；首次定义"仓库即记录系统"等核心原则
2. **Martin Fowler Harness Engineering**（2026.04.02）：赛博控制论框架；引入"前馈引导 + 反馈传感器"的正式模型

---

## Harness 的职责边界

| 职责域 | 负责方 | 内容 |
|---|---|---|
| 设计环境 | 人类工程师 | 规则文件、AGENTS.md、schema |
| 执行代码 | Agent | 实现、测试、提交 |
| 强制架构 | Harness（机械） | 自定义 linters、CI、结构测试 |
| 人类监督 | 人类 | 审查 PR、审批 lint 报告 |

---

## 发展趋势

随着 LLM 能力提升，旧 harness 中的某些组件会变得不再必要（当模型可以自己处理时）。但好的 AI 工程师会定期：
1. 去除不再"承重"的 harness 组件
2. 寻找模型新能力带来的新组合空间

> "有趣的 harness 组合空间不会缩小，而是在移动。" —— Anthropic Prithvi Rajasekaran

---

## 相关工具生态

见 [[awesome_agent_harness]]，包含：全生命周期平台、编排器、任务运行器、框架、运行时、知识/记忆工具。
