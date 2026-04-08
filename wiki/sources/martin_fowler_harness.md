---
title: 面向代码智能体用户的 Harness 工程 (Harness Engineering for Coding Agent Users)
tags: [智能体, 工程方法论, Martin_Fowler, 质量保证]
created: 2026-04-08
updated: 2026-04-08
sources: [raw/articles/martin_fowler_harness.md]
status: active
---

# 面向代码智能体用户的 Harness 工程

## 核心摘要
本文由 Thoughtworks 的 Birgitta Böckeler 撰写，发布于 Martin Fowler 的个人网站。文章提出了一个心理模型，用于通过 **前馈引导 (Feedforward Guides)** 和 **反馈传感器 (Feedback Sensors)** 来构建对 AI 生成代码的信任。核心观点是：**智能体 = 模型 + Harness (脚手架/治理环)**。

## 关键见解
1. **控制论模型**：将 Harness 视为一种控制论调节器。
   - **前馈 (Guides)**：在行动前预判并规避错误（如：编程规范、RAG 检索）。
   - **反馈 (Sensors)**：在行动后观察并自我修正（如：测试、Linter、AI 评审）。
2. **两类执行方式**：
   - **计算型 (Computational)**：确定性、由 CPU 运行（测试、类型检查）。快速、廉价且可靠。
   - **推理型 (Inferential)**：语义性、由 GPU/NPU 运行（LLM 评审）。慢、昂贵且具有概率性。
3. **人类的角色：转向循环 (The Steering Loop)**：
   - 人类的职责不是写代码，而是根据智能体的表现迭代 Harness。当错误重复出现时，通过改进控制手段来防止或检测。
4. **Harness 分类**：
   - **可维护性 Harness**：调节内部代码质量（最容易实现）。
   - **架构适配度 Harness**：检查架构特性（适应度函数）。
   - **行为 (Behaviour) Harness**：验证功能正确性（最难，目前的“大象”）。
5. **Ashby 定律的应用**：通过定义拓扑结构（Variety Reduction）降低系统的多样性，从而使 Harness 的构建变得可行。

## 关联概念与实体
- 概念：[[agent_harness]], [[feedforward_and_feedback]], [[computational_vs_inferential]], [[steering_loop]], [[ashby_law]]
- 实体：[[martin_fowler]], [[thoughtworks]], [[birgitta_bockeler]]

## 评价
这是目前关于 Harness Engineering 最系统、最具权威性的定义之一，将零散的 Agent 技巧提升到了控制论和工程方法论的高度。
