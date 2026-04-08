---
title: Harness Engineering
tags: [概念, AI, 架构]
created: 2026-04-07
updated: 2026-04-07
sources: 1
status: active
---
# Harness Engineering (脚手架工程)

Harness Engineering 是构建外围基础设施、约束和反馈循环以包围 AI 模型（将其转化为可靠的自主 Agent）的新兴软件工程学科。

## 核心公式
> **Agent = Model (大脑) + Harness (身体与护栏)**

## 核心组件设计
- **上下文压缩 (Context Compaction)**：防止长对话爆显存或导致 LLM “遗忘”。
- **状态持久化 (State Persistence)**：利用 Git 工作流或文件系统解决大模型的“失忆症”。
- **验证闭环 (Verification Loops)**：硬编码的脚本拦截器（如强制执行 `tsc`，不通过则自动驳回要求重写）。

## "Steering Loop" 理念
将大模型的每一次失败视为**系统/Harness的 Bug**，而不是 Prompt 的问题。修复方式是添加一个新的验证工具（Linter）或物理隔离区。

## 关联概念
- [[Agent_Engineering]]