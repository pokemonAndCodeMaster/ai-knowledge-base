---
title: Cognitive Gearing
tags: [概念, AI, Agent]
created: 2026-04-07
updated: 2026-04-07
sources: 1
status: active
---
# Cognitive Gearing (认知齿轮)

Cognitive Gearing 是由 [[Garry_Tan]] 在 [[Gstack]] 框架中提出的机制。

## 核心理念
不在一个 Prompt 中要求 AI 做所有事，而是在不同开发阶段切换 Agent 的**人设（Persona）**。这能防止模型被冲突的指令干扰，并强迫其聚焦于特定的质量关卡。

## 实践示例
- **CEO**：验证产品方向。
- **Engineering Manager**：锁定架构，防止幻觉。
- **Paranoid Senior Engineer**：在 review 模式下，强制 Agent 停止生成新逻辑，仅寻找边界漏洞和架构缺陷。