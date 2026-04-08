---
title: 智能体脚手架 (Agent Harness)
tags: [概念, 智能体, 系统架构]
created: 2026-04-08
updated: 2026-04-08
sources: [martin_fowler_harness]
status: active
---

# 智能体脚手架 (Agent Harness)

## 定义
**Agent Harness** 是指除了 AI 模型本身以外，包裹在智能体周围的所有基础设施、约束机制和反馈回路。

一个通用的公式是：
> **智能体 (Agent) = 模型 (Model) + Harness**

## 核心目标
1. **预防错误**：提高智能体在第一次尝试时就做对的概率。
2. **自动纠偏**：在结果到达人类眼前之前，尽可能自动修复问题（Self-Correction）。
3. **建立信任**：弥补 LLM 的非确定性（Non-determinism）和缺乏上下文理解的缺陷。

## 组成部分 (Martin Fowler 模型)
- **前馈引导 (Guides)**：行动前的干预。
- **反馈传感器 (Sensors)**：行动后的检测。

## 环境可脚手架化 (Harnessability)
并非所有环境都同样容易建立 Harness。良好的“环境可供性 (Ambient Affordances)”包括：
- 强类型语言。
- 清晰的模块边界。
- 抽象掉复杂细节的框架。

## 关联概念
- [[feedforward_and_feedback]]
- [[computational_vs_inferential]]
- [[steering_loop]]
- [[harness_engineering]]
