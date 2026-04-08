---
title: Harness Stack 分层架构（Agent Harness 的五层结构）
tags: [核心概念, harness-engineering, 系统架构, 工具栈]
created: 2026-04-08
updated: 2026-04-08
sources: 3
status: active
---

# Harness Stack 分层架构

**关联节点**：[[Agent Harness Engineering]] | [[Agent 工作流五大模式]] | [[渐进式上下文披露]] | [[awesome_agent_harness]]

---

## 五层技术栈

从高层（接近用户）到底层（基础设施）：

```
┌─────────────────────────────────────────┐
│  Layer 5: 全生命周期平台                │
│  (Chorus, Almirant, Paperclip)          │
│  需求 → 规格 → 实现 → 审批 → 交付      │
├─────────────────────────────────────────┤
│  Layer 4: Agent 编排器                  │
│  (Vibe Kanban, Emdash, Oh My CC)        │
│  并行执行 + worktree 隔离 + 吞吐优化    │
├─────────────────────────────────────────┤
│  Layer 3: 任务运行器                    │
│  (Symphony, Baton, Linear Harness)      │
│  Issue Tracker → Agent → PR            │
├─────────────────────────────────────────┤
│  Layer 2: Harness 框架 / 运行时         │
│  (Deep Agents, DeerFlow, OpenClaw)      │
│  可组合原语 + 持久记忆 + 技能系统       │
├─────────────────────────────────────────┤
│  Layer 1: Coding Agents（模型层）       │
│  (Claude Code, Codex, OpenCode...)      │
│  在 harness 设计中是可替换的"商品"      │
└─────────────────────────────────────────┘
```

---

## 关键洞察

> "在 harness engineering 中，agent 是商品——harness 才是差异化因素。" —— README

也就是说，哪个 coding agent 最好并不是关键问题。**围绕它构建什么样的约束和反馈系统，才是决定产出质量的核心变量。**

---

## 每层的核心问题

| 层级 | 核心问题 | 解决的关键痛点 |
|---|---|---|
| 全生命周期平台 | 从需求到交付如何形成闭环？ | 人类-Agent 协作模型 |
| 编排器 | 如何实现高吞吐量并行执行？ | worktree 隔离 + 互不干扰 |
| 任务运行器 | Issue 如何变成 PR？ | "人类掌舵，agent 执行" |
| 框架/运行时 | Agent 如何跨会话保持存活？ | 持久记忆 + 长时运行 |
| 模型层 | 代码是怎么写的？ | （这层已被视为商品） |

---

## 横切关注点（Cross-Cutting Concerns）

以下能力需要在多层中都有体现：

- **渐进式上下文披露**：在需要时发现信息，而非一次性加载
- **知识与记忆**：跨会话保持状态（claude-mem, cq, Honcho）
- **标准与协议**：MCP、ACP、AGENTS.md 实现互操作性
