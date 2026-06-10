---
title: "AgentScope工具与服务层"
domain: ["agent_engineering"]
type: "code_module"
tags: [AgentScope, Tool, Toolkit, ToolBase, FastAPI, Agent Service]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "agentscope/src/agentscope/tool/"
  - "agentscope/src/agentscope/app/"
code_hash: ""
affects_path: []
trigger_keywords:
  - Toolkit
  - ToolBase
  - ToolChoice
  - Agent Service
  - create_app
  - ChatService
---

# AgentScope工具与服务层

## 工具系统 (`tool/`)

### 内置工具

从骨架可见的内置工具集：

```python
from agentscope.tool import (
    Bash,      # Shell 命令执行
    Grep,      # 文本搜索
    Glob,      # 文件模式匹配
    Read,      # 文件读取
    Write,     # 文件写入
    Edit,      # 文件编辑
    Toolkit,   # 工具容器
)
```

### 工具抽象

```python
class ToolBase:
    """所有工具的基类"""
    # 子类实现 execute() 方法
    # Pydantic BaseModel 定义参数 Schema
    # PermissionBehavior 定义权限行为

class Toolkit:
    """工具容器，管理工具集合"""
    # 注册工具 → 生成 JSON Schema → 供 LLM 调用

class ToolChoice:
    """LLM 的工具选择配置"""
    # auto / none / required / 指定工具

class ToolResponse:
    """工具执行结果"""
    # 包含 state, chunks, usage
```

### 工具流式响应

```python
class ToolChunk:
    """工具执行的增量输出"""
    # 支持流式返回，大结果不阻塞
```

## 服务层 (`app/`)

### FastAPI 服务架构

```
create_app()
  ├── Routers:
  │   ├── agent_router   → Agent CRUD
  │   ├── chat_router    → 聊天触发
  │   ├── session_router → 会话管理
  │   ├── schedule_router → 定时任务
  │   ├── credential_router → 凭证管理
  │   ├── model_router   → 模型管理
  │   └── workspace_router → 工作空间
  │
  ├── Services:
  │   ├── ChatService    → 核心对话服务
  │   └── SessionService → 会话生命周期
  │
  └── Managers:
      ├── BackgroundTaskManager → 后台任务
      ├── SchedulerManager     → Cron 调度
      ├── WakeupDispatcher     → 跨会话唤醒
      ├── CancelDispatcher     → 跨进程取消
      └── ChatRunRegistry      → 运行中任务注册
```

### 多租户隔离

- 每个用户有独立的 Agent 和 Session
- `get_current_user_id()` 依赖注入
- 会话级别的工具权限配置

### Agent Team

> 引用自 README.md：
> "a leader agent spawns workers and coordinates them through the built-in team tools."

Team 实现了多 Agent 协作的标准模式：
- Leader Agent 拆解任务
- 动态 spawn Worker Agent
- 通过 Team Tools 协调
