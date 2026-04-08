---
title: Martin Fowler：Harness Engineering for Coding Agent Users
tags: [来源摘要, harness-engineering, 赛博控制论, 反馈系统, Martin-Fowler]
created: 2026-04-08
updated: 2026-04-08
sources: 1
source_url: https://martinfowler.com/articles/harness-engineering.html
source_type: article
status: active
---

# Martin Fowler：Harness Engineering for Coding Agent Users

**关联节点**：[[Agent Harness Engineering]] | [[前馈与反馈控制]] | [[可维护性Harness]] | [[赛博控制论与Harness]] | [[Birgitta Böckeler]]

---

## 文章地位

本文（2026 年 4 月 2 日）是 Harness Engineering 领域的**权威工业参考**，发表于 Martin Fowler 的个人技术博客。作者 Birgitta Böckeler 是 Thoughtworks 的杰出工程师（Distinguished Engineer）。

---

## 核心框架：前馈 + 反馈

| 控制类型 | 作用时机 | 目的 |
|---|---|---|
| **Guides（引导）** | agent 行动前 | 增加首次产出好结果的概率 |
| **Sensors（传感器）** | agent 行动后 | 帮助 agent 自我纠正 |

---

## 执行类型：计算型 vs 推理型

| 类型 | 执行主体 | 速度 | 可靠性 | 示例 |
|---|---|---|---|---|
| **计算型** | CPU | 毫秒级 | 确定性 | 测试、linters、类型检查 |
| **推理型** | GPU/NPU | 慢且贵 | 非确定性 | AI 代码审查、LLM as judge |

---

## 三类调节范畴

1. **可维护性 Harness**：内部代码质量（最成熟，工具最多）
2. **架构适应性 Harness**：架构特性和约束（Fitness Functions）
3. **行为 Harness**：功能行为验证（最困难，仍是开放问题）

---

## 核心洞察

- **质量左移**：越早发现问题，修复越便宜。检查应按成本/速度拆分到开发生命周期各阶段
- **Ambient Affordances**：环境的结构性属性决定了 agent 的可驾驭性
- **Harnessability**：强类型语言的代码库比弱类型更易驾驭
- **Ashby 必要多样性定律**：限定服务拓扑（topology）是降低多样性的举措，使 harness 更易实现

---

## 与 OpenAI Harness Engineering 的关联

Fowler 文章明确引用并印证了 OpenAI 在自己团队实践中的发现：
> "我们最困难的挑战现在集中在设计环境、反馈循环和控制系统上。"
