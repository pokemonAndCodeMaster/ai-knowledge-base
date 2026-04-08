# Harness Engineering for Coding Agent Users（原文存档）

> Source: https://martinfowler.com/articles/harness-engineering.html
> Author: Birgitta Böckeler (Thoughtworks Distinguished Engineer)
> Published: 02 April 2026

A mental model for building trust in coding agents through feedforward guides, feedback sensors, and iterative harness engineering.

## 核心定义

Agent = Model + Harness。Harness 是除模型本身以外的一切。

## Feedforward and Feedback（前馈与反馈）

- **Guides（前馈控制）**：预测 agent 的行为，在其行动前引导它。提高首次产出好结果的概率。
- **Sensors（反馈控制）**：在 agent 行动后观测，帮助其自我纠正。特别强大的传感器会产生针对 LLM 消费优化的信号，例如包含自我纠正指令的自定义 linter 消息。

## Computational vs Inferential（计算型 vs 推理型）

- **计算型（Computational）**：确定性，速度快，由 CPU 运行。包括测试、linters、类型检查、结构分析。毫秒级，结果可靠。
- **推理型（Inferential）**：语义分析，AI 代码审查，"LLM as judge"。GPU/NPU 运行。更慢更贵；结果更不确定。

## The Steering Loop（引导循环）

人类的工作是通过迭代 harness 来引导 agent。每次问题重复出现，都应该改进前馈和反馈控制，让问题在未来不太可能出现。

## Timing: Keep Quality Left（质量左移）

- 在集成前甚至提交前：运行速度快的检查（linters、快速测试、基础代码审查 agent）
- 更昂贵的检查放在流水线后期（变异测试、更宏观的代码审查）
- 持续漂移传感器：对代码库持续运行（死代码检测、测试覆盖率分析）

## Regulation Categories（调节类别）

### 1. Maintainability Harness（可维护性 Harness）
使用已有工具对内部代码质量进行调节。计算型传感器可靠捕获结构性问题（重复代码、圈复杂度、架构漂移）。

### 2. Architecture Fitness Harness（架构适应性 Harness）
定义并检查应用的架构特性。类似 Fitness Functions。

### 3. Behaviour Harness（行为 Harness）
如何引导和感知应用是否按需工作？这是目前最难解决的一类 Harness。

## Ambient Affordances（环境可供性）

"ambient affordances" = 使 agent 环境更可被驾驭的结构性属性：让环境对 agent 更清晰、更可导航、更可处理。

对于全新代码库：可以从第一天就内建可被驾驭性。
对于遗留代码库：Harness 最需要的地方，往往也是最难构建的地方。

## Harness Templates（Harness 模板）

企业可能会为常见服务拓扑（业务服务、事件处理、数据仪表板等）制定 Harness 模板——包含 guides 和 sensors 的捆绑包。

## Ashby's Law

Ashby 必要多样性定律：调节器必须至少拥有与被调节系统同等多的多样性。限定拓扑是降低多样性的举措，使全面的 Harness 更易实现。

## The Role of the Human

一名人类开发者把技能和经验作为隐式 Harness 带进每个代码库。Harness 是外显这种人类开发者经验的尝试，但只能做到一定程度。好的 Harness 不应该完全消除人类输入，而是应该把人类的输入引导到最重要的地方。
