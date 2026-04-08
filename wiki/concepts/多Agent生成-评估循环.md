---
title: 多 Agent 生成-评估循环（GAN 启发的多 Agent 架构）
tags: [核心概念, harness-engineering, multi-agent, 评估器, 生成器]
created: 2026-04-08
updated: 2026-04-08
sources: 2
status: active
---

# 多 Agent 生成-评估循环

**关联节点**：[[Agent 工作流五大模式]] | [[前馈与反馈控制]] | [[anthropic_harness_design_long_running]] | [[Sprint合同模式]] | [[Context Reset vs Compaction]]

---

## 核心思想

受 GAN（生成对抗网络）启发：将生成器与评估器分离，形成反馈循环。

> **关键洞察**：让独立 agent 进行批判，比让同一 agent 批判自己的产出容易得多。

---

## 架构图

```
用户提示（1-4句）
    ↓
[Planner] 扩展为完整产品规格
    ↓
[Generator] ←──────────────────────────────────┐
    │  实现 Sprint N                             │
    ↓                                            │
[Sprint Contract 协商]                           │
    ↓                                            │
[Evaluator] 像用户一样测试（Playwright MCP）      │
    │  通过 ──────── 完成 Sprint N               │
    │  失败 ──── 提供具体反馈 ──────────────────┘
    ↓（所有 Sprint 完成）
最终产品
```

---

## 三个 Agent 的角色

### Planner（规划者）
- 输入：1-4 句话的简短提示
- 输出：完整的产品规格（高层次）
- 原则：约束交付**产物**，不约束**路径**（避免规格错误级联到实现）

### Generator（生成者）
- Sprint 制工作，每次一个功能
- Sprint 结束后自我评估，再交给 Evaluator
- 每个 sprint 前与 Evaluator 协商 Sprint Contract

### Evaluator（评估者）
- 使用 Playwright MCP 像用户一样点击运行中的应用
- 对每个评分维度设有硬性门槛
- 提供具体到可操作的反馈（不是"有问题"而是"第892行 fillRectangle 调用错误"）

---

## Sprint Contract（Sprint 合同）

每个 sprint 开始前的"预协商"：
1. Generator 提议：将构建什么 + 如何验证成功
2. Evaluator 审查提议，确保目标对齐
3. 两者协商直到共同确认"完成"的定义

---

## 为什么分离生成器和评估器？

| 场景 | 单 Agent | 分离后 |
|---|---|---|
| 主观质量判断 | 自我赞美偏差（总说好） | 可调整成批判性 |
| 功能验证 | 可能绕过验证 | Playwright 实测 |
| 错误检测 | 混淆"工作"与"正确" | 独立 QA 视角 |

---

## 适用时机

此架构在任务**超出模型独立处理能力边界**时最有价值。当模型能力提升，某些 sprint 内的工作会回落到模型自身能力范围内，此时 Evaluator 的价值降低——应定期重新评估 harness 是否"过重"。
