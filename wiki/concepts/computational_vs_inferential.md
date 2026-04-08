---
title: 计算型控制与推理型控制 (Computational vs Inferential Controls)
tags: [概念, 智能体, 工程效率]
created: 2026-04-08
updated: 2026-04-08
sources: [martin_fowler_harness]
status: active
---

# 计算型控制与推理型控制 (Computational vs Inferential Controls)

在设计 Harness 的传感器和引导器时，需要根据执行效率和确定性将其分类：

## 1. 计算型 (Computational)
**执行者**：CPU。
**特点**：
- **确定性**：结果是可预测的，非黑即白。
- **极速**：以毫秒到秒为单位运行。
- **廉价**：本地运行，几乎不产生 Token 成本。
**例子**：
- 静态分析 (Linters)。
- 类型检查 (Type Checkers)。
- 单元测试 (Test Suites)。
- 结构性适配度函数。

## 2. 推理型 (Inferential)
**执行者**：GPU / NPU (由 LLM 驱动)。
**特点**：
- **非确定性**：结果具有概率性，可能存在幻觉。
- **慢速**：需要网络请求或大規模推理，速度随 Token 增加而变慢。
- **昂贵**：消耗 API 成本。
**例子**：
- **AI 代码评审**：检查语义逻辑和设计模式。
- **LLM as Judge**：由模型对输出质量进行评分。
- **语义搜索/相关性排序**。

## 权衡建议 (Pledge)
尽可能将 **计算型** 传感器作为第一道防线，因为它们提供了 100% 的确定性。推理型传感器应用于捕捉人类直觉和高级语义问题，且不宜在每次 Commit 时高频运行（除非成本极低）。

## 关联概念
- [[feedforward_and_feedback]]
- [[agent_harness]]
