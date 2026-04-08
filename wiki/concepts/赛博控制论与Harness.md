---
title: 赛博控制论与 Harness Engineering
tags: [核心概念, harness-engineering, 控制论, 历史溯源]
created: 2026-04-08
updated: 2026-04-08
sources: 2
status: active
---

# 赛博控制论与 Harness Engineering

**关联节点**：[[Agent Harness Engineering]] | [[前馈与反馈控制]] | [[martin_fowler_harness_engineering]]

---

## 核心类比

Martin Fowler 将 Agent Harness 定义为**赛博控制论意义上的调节器（Cybernetic Governor）**。

历史溯源：
- **James Watt（蒸汽机调速器）**：用离心力机械地调节蒸汽机速度 → 前馈+反馈的工程实现
- **Norbert Wiener（控制论之父）**：提出"控制与通信"作为系统调节的统一理论
- **今天的 LLM Harness**：在架构层面关闭反馈循环 → 通过机器可读规范将人类判断外化

---

## ACI（Agent-Computer Interface）

类比 HCI（Human-Computer Interface），Anthropic 提出：

> "设计 agent 的动作空间，与设计好的用户界面需要同等程度的工程投入。"

**ACI 设计原则**：
1. 给模型足够的 tokens 在"写进死角"之前先思考
2. 格式贴近模型在互联网上自然见到的内容
3. 避免格式"开销"（如需精确计数的场景）
4. 站在模型角度考虑工具是否直观
5. Poka-yoke（防错）：让错误输入更难发生

---

## Ashby 必要多样性定律

> 调节器必须拥有至少与被调节系统同等多的"多样性"（variety），才能控制它。调节器只能调节它拥有模型的东西。

**在 Agent Harness 中的含义**：

LLM coding agent 几乎可以产生任何输出（超高多样性）。通过：
1. 定义标准服务拓扑（topology）
2. 规定编码约定和架构约束

→ 将可能输出的空间**缩小**到 harness 可以全面覆盖的范围。

这是"为什么限制反而能提升可靠性"的理论依据。

---

## 与其他领域控制论实践的对比

| 领域 | 调节器 | 前馈 | 反馈 |
|---|---|---|---|
| 工业控制 | PID 控制器 | 设定点 | 传感器读数 |
| DevOps | CI/CD 流水线 | 测试、linters | 生产监控 |
| **LLM Harness** | **Agent Harness** | **AGENTS.md、skills/** | **测试结果、linters、AI评审** |
