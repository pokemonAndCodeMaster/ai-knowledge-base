---
title: Awesome Agent Harness（GitHub 精选列表）
tags: [来源摘要, agent-harness, 工具生态, 综合索引]
created: 2026-04-08
updated: 2026-04-08
sources: 1
source_url: https://github.com/AutoJunjie/awesome-agent-harness
source_type: github
status: active
---

# Awesome Agent Harness（GitHub 精选列表）

**关联节点**：[[Agent Harness Engineering]] | [[Harness Stack 分层架构]] | [[渐进式上下文披露]] | [[AGENTS.md 标准]]

---

## 核心定义

**Agent Harness** = 包裹 LLM coding agent 的基础设施。涵盖除模型本身以外的一切：会话管理、上下文交付、工具设计、架构强制、故障恢复和人类监督。

> "当一个软件工程团队的主要工作不再是编写代码，而是设计环境、指定意图，并构建能让 agent 可靠工作的反馈循环。" —— OpenAI Harness Engineering

---

## 8 项核心原则

1. **人类掌舵，agent 执行** — 工程师设计环境、审查结果，不再写代码
2. **仓库知识是记录系统** — 不在仓库里的东西对 agent 不可见
3. **AGENTS.md 是目录而非百科全书** — 指向更深的真相来源
4. **机械强制架构** — 自定义 linters、结构测试、CI 检查
5. **Agent 可读性是目标** — 先优化 agent 可读性，再考虑人类可读性
6. **更少工具，更强表达力** — 可组合原语 > 大量工具
7. **像 Agent 一样观察** — 读取模型输出，观察挣扎点，演化 harness
8. **修正便宜，等待昂贵** — 高吞吐量下，fix-forward > 阻塞合并门

---

## 工具生态全景（按层分类）

### 全生命周期平台
- **Chorus**：需求到交付，含 Task DAG 和人类审批门
- **Almirant**：人类-agent 团队操作系统，跨会话持久上下文
- **Paperclip**：零人类公司的开源编排，全自主操作

### Agent 编排器
- **Vibe Kanban**：每个 agent 独立 git worktree 的看板编排
- **Emdash (YC W26)**：并行 agents 在隔离 worktrees，支持远程
- **Oh My Claude Code**：Ultrapilot 模式，5 个 Claude Code 并行运行，将 4 小时任务压缩到 50 分钟

### 任务运行器（Issue→PR 管道）
- **Symphony (OpenAI)**：参考实现。轮询 Linear issues → 产出 PRs
- **Axon**：Kubernetes 原生，Task CRD → PR + 成本报告

### Harness 框架
- **Deep Agents (LangChain)**：通过规划工具和子 agent 衍生实现渐进式上下文披露
- **DeerFlow 2.0 (ByteDance)**：技能系统 + 按需加载 + 持久记忆
- **Zylos**：Claude Code 的持久 harness，分层记忆系统
- **Meta-Harness**：学术方法，用 Claude Code 端到端优化 harness

### Agent 运行时
- **OpenClaw**：跨消息频道编排 agents，含技能系统和持久会话

### 知识与记忆
- **claude-mem**：自动会话捕获、AI 压缩和注入
- **cq (Mozilla)**：agents 共享学习知识的公共库
- **Honcho**：agent 状态记忆库，会话历史和用户上下文

### 标准与协议
- **MCP (Model Context Protocol)**：连接 AI 模型到外部工具的开放标准
- **ACP (Agent Communication Protocol)**：agent 间和 agent-harness 通信协议
- **GitAgent**：git 原生标准：agent.yaml + SOUL.md + RULES.md

### 方法论与工作流
- **AI-DLC (AWS)**：AI 驱动开发生命周期，三阶段：理解 → 规划 → 构建

---

## 权威参考文章

| 文章 | 来源 | 核心贡献 |
|---|---|---|
| Harness Engineering | OpenAI 博客 | 定义领域，1M+ 行零人工代码案例 |
| Building Effective Agents | Anthropic | 五种可组合工作流模式 |
| Harness Engineering | Martin Fowler | 赛博内控模型（前馈+反馈+计算/推理型） |
| Harness Design for Long-Running Apps | Anthropic | 多 agent 架构（规划/生成/评估）+ Sprint 合同 |
| Anatomy of an Agent Harness | LangChain | Agent = Model + Harness 的解剖学 |
