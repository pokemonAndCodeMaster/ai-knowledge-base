---
title: Ashby 必备多样性定律 (Ashby's Law of Requisite Variety)
tags: [概念, 控制论, 智能体]
created: 2026-04-08
updated: 2026-04-08
sources: [martin_fowler_harness]
status: active
---

# Ashby 必备多样性定律 (Ashby's Law of Requisite Variety)

## 基本定义
由 W. Ross Ashby 提出，控制论的关键原则：
> **只有多样性 (Variety) 能够吸收多样性。**

简单来说，如果一个调节器（控制系统）要稳定一个系统，调节器必须具备至少与被调节系统一样多的应对状态（多样性）。

## 在 Harness Engineering 中的应用
- **问题**：LLM 几乎可以产生“任何”代码（无限的多样性），这使得构建一个完美的、通用的 Harness 变得极其困难。
- **解决方案**：**多样性缩减 (Variety Reduction)**。
  - 通过定义固定的**拓扑结构 (Topologies)** 或 **Harness 模板 (Templates)** 来约束系统的状态空间。
  - 例如，强制要求某个服务只能使用特定的技术栈和分层架构。一旦多样性被缩减到可管理的范围，Harness 就能够更有效地对其进行治理。

## 结论
一个智能体系统的可控性，取决于我们对该系统规则的定义清晰度以及多样性的约束程度。

## 关联概念
- [[agent_harness]]
- [[harness_templates]]
