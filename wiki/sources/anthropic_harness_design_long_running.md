---
title: Anthropic：长时运行应用的 Harness 设计
tags: [来源摘要, harness-design, multi-agent, 上下文管理, Anthropic]
created: 2026-04-08
updated: 2026-04-08
sources: 1
source_url: https://www.anthropic.com/engineering/harness-design-long-running-apps
source_type: article
status: active
---

# Anthropic：长时运行应用的 Harness 设计

**关联节点**：[[多Agent生成-评估循环]] | [[Context Reset vs Compaction]] | [[Sprint合同模式]] | [[Agent Harness Engineering]]

---

## 解决的核心问题

1. **Context Anxiety（上下文焦虑）**：模型接近其认为的上下文限制时，过早结束工作
2. **自我评估偏差**：agent 评估自身产出时倾向于过度肯定

---

## 核心架构：三 Agent 系统

### Planner（规划者）
- 将 1-4 句话的提示扩展为完整产品规格
- 聚焦高层次产品上下文和技术设计，不涉及详细实现
- 原则：给 agent 约束要交付的产物，让它们自行找路径

### Generator（生成者）
- Sprint 制工作，每次实现一个功能
- Sprint 结束后自我评估，再交给 Evaluator
- 每个 sprint 前与 Evaluator 协商 Sprint Contract

### Evaluator（评估者）
- 使用 Playwright MCP 像用户一样点击运行中的应用
- 评分标准（从前端实验迁移）：产品深度、功能性、视觉设计、代码质量
- 每个标准有硬性门槛，任意未达标则 sprint 失败并反馈详情

---

## Sprint Contract（Sprint 合同）模式

每个 sprint 开始前，生成器和评估器**协商"完成"的定义**：
- 生成器提议将构建什么以及如何验证成功
- 评估器审查提议，确保生成器在构建正确的东西
- 两者协商迭代直到达成共识

> 核心价值：将高层次规格与可测试实现之间的鸿沟桥接起来

---

## Context Reset vs Compaction

| 方法 | 机制 | 优点 | 缺点 |
|---|---|---|---|
| **Compaction** | 原位总结较早对话 | 保持连续性 | context anxiety 仍可能持续 |
| **Context Reset** | 完全清除上下文，启动新 agent | 干净的起点 | 需要丰富的 handoff artifact |

---

## 关键原则：Harness 的进化论

> 每个 harness 组件都编码了对模型无法独自完成的某件事的假设。这些假设值得持续压力测试。

**随着模型改进，好的 AI 工程师会定期去除不再"承重"的组件，并找到新的能力组合。**

---

## 前端设计实验：让主观质量可量化

四个评分标准：
- **设计质量**：整体感，而非零件的组合
- **原创性**：是否有自定义决策，而非模板和 AI 模式
- **工艺**：技术执行（排版、间距、色彩）
- **功能性**：可用性，独立于美学

重要：评分标准的**措辞**本身会引导生成方向（包含"博物馆级别"会引发视觉收敛）
