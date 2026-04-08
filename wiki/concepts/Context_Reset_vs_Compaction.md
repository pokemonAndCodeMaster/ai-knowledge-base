---
title: Context Reset vs Compaction（上下文重置 vs 压缩）
tags: [核心概念, harness-engineering, 上下文管理, 长时运行]
created: 2026-04-08
updated: 2026-04-08
sources: 1
status: active
---

# Context Reset vs Compaction

**关联节点**：[[多Agent生成-评估循环]] | [[anthropic_harness_design_long_running]] | [[Agent Harness Engineering]]

---

## 背景：Context Anxiety（上下文焦虑）

当 LLM 接近其认为的上下文限制时，会**过早结束工作**——即使仍有能力继续。这是长时运行 coding agent 的核心挑战之一。

---

## 两种解决策略

| 特性 | Compaction（压缩） | Context Reset（重置） |
|---|---|---|
| **机制** | 对较早对话部分进行原位总结 | 完全清除上下文，启动新 agent |
| **连续性** | ✅ 保持 | ❌ 中断，依赖 handoff artifact |
| **context anxiety** | ❌ 仍可能出现 | ✅ 根本解决 |
| **开销** | 低 | 高（handoff artifact + token 开销 + 延迟） |
| **实现复杂度** | 低 | 高（需要设计 handoff 协议） |

---

## 什么时候用哪种？

**Compaction 适用**：
- 模型上下文焦虑程度较低（如 Opus 4.6）
- 任务不需要极长的持续时间
- 追求较低的 token 成本

**Context Reset 适用**：
- 模型上下文焦虑严重（如早期的 Sonnet 4.5）
- 需要多小时的自主工作会话
- 宁肯增加复杂度也要保证 agent 不提前放弃

---

## Handoff Artifact 的关键设计

使用 Context Reset 时，handoff artifact 需要包含：
- 当前已完成的工作状态
- 未完成的工作列表
- 关键的设计决策和约束条件
- 下一步计划

> Agent 之间的通信通过**文件**实现：一个 agent 写文件，另一个读之后响应。保持了状态，但不共享上下文窗口。

---

## 随模型演进的变化

Anthropic 在实践中发现：当 Opus 4.5 升级到 Opus 4.6 后，context anxiety 显著降低，可以去掉 Context Reset，改用 Compaction，大幅降低了 harness 复杂度。

这印证了核心原则：**定期重新评估 harness，去除不再"承重"的组件。**
