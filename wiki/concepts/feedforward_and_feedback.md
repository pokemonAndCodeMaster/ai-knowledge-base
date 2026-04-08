---
title: 前馈引导与反馈传感器 (Feedforward and Feedback)
tags: [概念, 控制论, 智能体]
created: 2026-04-08
updated: 2026-04-08
sources: [martin_fowler_harness]
status: active
---

# 前馈引导与反馈传感器 (Feedforward and Feedback)

这是 Harness Engineering 的两个核心调节器，灵感来源于物理学和控制论。

## 1. 前馈引导 (Feedforward Guides)
**定义**：在智能体开始行动（生成代码或执行任务）之前，预先注入的控制指令。

**目标**：提高“一次性成功率”。

**例子**：
- **系统提示词 (System Prompts)**：规定代码风格和质量要求。
- **RAG 检索 (Retrieval)**：提供相关的代码上下文、库文档。
- **编码规范 (Coding Standards)**：在上下文中显式声明。
- **LSP / 代码补全**：提供静态的补全建议。

## 2. 反馈传感器 (Feedback Sensors)
**定义**：在智能体行动之后，观察其输出并提供修正信号。

**目标**：实现“自动纠错 (Self-correction)”。

**例子**：
- **Linter / 类型检查**：检测语法或逻辑错误。
- **单元测试 / 集成测试**：验证功能正确性。
- **架构检查 (Fitness Functions)**：检查是否违反了架构规则。
- **AI 裁判 (LLM Audit)**：由另一个模型对代码进行语义评审。

## 协同效用
- **仅前馈**：无法得知规则是否被遵守，容易产生幻觉。
- **仅反馈**：智能体可能会盲目试错，浪费 Token 且效率低下。
- **前馈 + 反馈**：形成完整的闭环调节系统。

## 关联概念
- [[agent_harness]]
- [[steering_loop]]
