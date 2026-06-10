---
title: "agentscope_source_docs"
domain: ["agent_engineering"]
type: "source"
tags: [AgentScope, README, 骨架]
created: 2026-06-10
updated: 2026-06-10
status: active
original_path: "agentscope/README.md + agentscope/src/"
content_hash: ""
---

# AgentScope 文档来源记录

## 原文位置
- `agentscope/README.md` (272 行)
- `agentscope/src/agentscope/` (215 文件，骨架提取)

## 核心内容提炼

### README.md
- AgentScope 2.0 生产级 Agent 框架
- 五大系统：Event / Permission / Multi-tenancy / Workspace / Middleware
- 设计哲学：利用 LLM 能力而非约束
- Agent Team：Leader-Worker 协作模式
- 阿里巴巴出品，ArXiv 论文

### 代码骨架 (215 文件)
- `agent/`：统一 Agent 类 + ReAct 配置
- `app/`：FastAPI 多租户服务 (7 Router + 2 Service + 5 Manager)
- `tool/`：工具系统 (Bash/Grep/Glob/Read/Write/Edit)
- `permission/`：三级权限 (Bypass/Confirm/Deny)
- `event/`：30+ 事件类型的统一事件总线
- `middleware/`：可组合中间件系统
- `model/`：多供应商模型适配
- `workspace/`：沙箱环境 (Local/Docker/E2B)

## 分解出的知识卡片
- [[AgentScope项目]] (entity)
- [[Agent权限系统]] / [[Event驱动Agent架构]] (concept × 2)
- [[AgentScope工具与服务层]] (code_module)
