# 🦴 代码目录架构骨架 (Code Skeleton)

> 提取目标: `agentscope/src/agentscope/`
> 共包含 215 个代码文件

## 📄 agentscope/src/agentscope/__init__.py
> **模块说明**: The agentscope serialization module

### 📦 依赖 (Imports)
- `import warnings`
- `from _logging import logger`
- `from _logging import setup_logger`
- `from _version import __version__`

---

## 📄 agentscope/src/agentscope/_logging.py
> **模块说明**: The logger for agentscope.

### 📦 依赖 (Imports)
- `import logging`

### ⚡ 函数 (Functions)
- `def setup_logger(...):`

---

## 📄 agentscope/src/agentscope/_utils/__init__.py

---

## 📄 agentscope/src/agentscope/_utils/_audio.py
> **模块说明**: Audio utilities shared across model providers.

### 📦 依赖 (Imports)
- `import struct`

### ⚡ 函数 (Functions)
- `def _build_streaming_wav_header(...):`

---

## 📄 agentscope/src/agentscope/_utils/_common.py
> **模块说明**: The common utilities for agentscope library.

### 📦 依赖 (Imports)
- `import asyncio`
- `import base64`
- `import functools`
- `import inspect`
- `import json`
- `import os`
- `import types`
- `import uuid`
- `from datetime import datetime`
- `from typing import Any`
- `from typing import Callable`
- `import requests`
- `from json_repair import repair_json`
- `from _logging import logger`
- `from exception import ToolJSONDecodeError`

### ⚡ 函数 (Functions)
- `def _json_loads_with_repair(...):`
- `def _get_timestamp(...):`
- `def _get_bytes_from_web_url(...):`
- `def _map_text_to_uuid(...):`

---

## 📄 agentscope/src/agentscope/_utils/_mixin.py
> **模块说明**: The mixin for agentscope.

### 🏗️ 类 (Classes)
- `class DictMixin(dict):`

---

## 📄 agentscope/src/agentscope/_version.py
> **模块说明**: The version of agentscope.

---

## 📄 agentscope/src/agentscope/agent/__init__.py
> **模块说明**: Initialize the agent module.

### 📦 依赖 (Imports)
- `from _agent import Agent`
- `from _config import ContextConfig`
- `from _config import ModelConfig`
- `from _config import ReActConfig`

---

## 📄 agentscope/src/agentscope/agent/_agent.py
> **模块说明**: The unified agent class in AgentScope library.

### 📦 依赖 (Imports)
- `import asyncio`
- `import inspect`
- `import uuid`
- `from asyncio import Queue`
- `from copy import deepcopy`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import Sequence`
- `from typing import Literal`
- `from typing import List`
- `from typing import TYPE_CHECKING`
- `import jsonschema`
- `from _config import ContextConfig`
- `from _config import ReActConfig`
- `from _config import ModelConfig`
- `from state import AgentState`
- `from _utils import _ToolCallBatch`
- `from _logging import logger`
- `from _utils._common import _json_loads_with_repair`
- `from event import AgentEvent`
- `from event import ModelCallEndEvent`
- `from event import ModelCallStartEvent`
- `from event import ReplyEndEvent`
- `from event import ReplyStartEvent`
- `from event import TextBlockDeltaEvent`
- `from event import TextBlockEndEvent`
- `from event import TextBlockStartEvent`
- `from event import ThinkingBlockDeltaEvent`
- `from event import ThinkingBlockEndEvent`
- `from event import ThinkingBlockStartEvent`
- `from event import ToolCallDeltaEvent`
- `from event import ToolCallEndEvent`
- `from event import ToolCallStartEvent`
- `from event import ToolResultDataDeltaEvent`
- `from event import ToolResultEndEvent`
- `from event import ToolResultStartEvent`
- `from event import ToolResultTextDeltaEvent`
- `from event import RequireUserConfirmEvent`
- `from event import RequireExternalExecutionEvent`
- `from event import ExternalExecutionResultEvent`
- `from event import UserConfirmResultEvent`
- `from event import DataBlockStartEvent`
- `from event import DataBlockDeltaEvent`
- `from event import DataBlockEndEvent`
- `from event import ExceedMaxItersEvent`
- `from exception import AgentOrientedException`
- `from model import ChatResponse`
- `from model import ChatUsage`
- `from model import ChatModelBase`
- `from message import Msg`
- `from message import AssistantMsg`
- `from message import SystemMsg`
- `from message import UserMsg`
- `from message import TextBlock`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`
- `from message import DataBlock`
- `from message import Base64Source`
- `from message import URLSource`
- `from message import ToolCallState`
- `from message import ToolResultState`
- `from message import Usage`
- `from tool import Toolkit`
- `from tool import ToolChunk`
- `from tool import ToolChoice`
- `from tool import ToolResponse`
- `from permission import PermissionBehavior`
- `from permission import PermissionEngine`
- `from permission import PermissionDecision`
- `from workspace import Offloader`
- `from workspace import WorkspaceBase`

### 🏗️ 类 (Classes)
- `class Agent:`
- `    def __init__(...):`
- `    def _update_tool_call_state(...):`
- `    def _save_to_context(...):`
- `    def _get_last_msg(...):`
- `    def _check_next_action(...):`
- `    def _get_executable_tool_calls(...):`

---

## 📄 agentscope/src/agentscope/agent/_config.py
> **模块说明**: The agent config classes.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from model import ChatModelBase`

### 🏗️ 类 (Classes)
- `class SummarySchema(BaseModel):`
- `class ContextConfig(BaseModel):`
- `class ReActConfig(BaseModel):`
- `class ModelConfig(BaseModel):`

---

## 📄 agentscope/src/agentscope/agent/_utils.py
> **模块说明**: The utility classes used in building the agent class.

### 📦 依赖 (Imports)
- `from dataclasses import dataclass`
- `from typing import Literal`
- `from message import ToolCallBlock`

### 🏗️ 类 (Classes)
- `class _ToolCallBatch:`

---

## 📄 agentscope/src/agentscope/app/__init__.py
> **模块说明**: The FastAPI based agent service module, which contains all service-related

### 📦 依赖 (Imports)
- `from _app import create_app`
- `from _types import SubAgentTemplate`

---

## 📄 agentscope/src/agentscope/app/_app.py
> **模块说明**: AgentScope app factory.

### 📦 依赖 (Imports)
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from typing import Any`
- `from _lifespan import lifespan`
- `from workspace_manager import WorkspaceManagerBase`
- `from _router import agent_router`
- `from _router import chat_router`
- `from _router import credential_router`
- `from _router import model_router`
- `from _router import schedule_router`
- `from _router import session_router`
- `from _router import workspace_router`
- `from _types import AgentMiddlewareFactory`
- `from _types import AgentToolFactory`
- `from _types import SubAgentTemplate`
- `from message_bus import MessageBus`
- `from storage import StorageBase`
- `from agent import Agent`
- `from credential import CredentialFactory`
- `from credential import CredentialBase`
- `from _version import __version__`

### ⚡ 函数 (Functions)
- `def create_app(...):`

---

## 📄 agentscope/src/agentscope/app/_lifespan.py
> **模块说明**: The lifespan of the agent service.

### 📦 依赖 (Imports)
- `from contextlib import AsyncExitStack`
- `from contextlib import asynccontextmanager`
- `from typing import TYPE_CHECKING`
- `from typing import Any`
- `from typing import AsyncIterator`
- `from _manager import BackgroundTaskManager`
- `from _manager import CancelDispatcher`
- `from _manager import ChatRunRegistry`
- `from _manager import SchedulerManager`
- `from _manager import WakeupDispatcher`
- `from _service import ChatService`
- `from _service import SessionService`

---

## 📄 agentscope/src/agentscope/app/_manager/__init__.py
> **模块说明**: The agent service managers, used in FastAPI lifespan to manage

### 📦 依赖 (Imports)
- `from _scheduler import SchedulerManager`
- `from _wakeup_dispatcher import WakeupDispatcher`
- `from _cancel_dispatcher import CancelDispatcher`
- `from _chat_run_registry import ChatRunRegistry`
- `from _background_task_manager import BackgroundTaskManager`

---

## 📄 agentscope/src/agentscope/app/_manager/_background_task_manager.py
> **模块说明**: The background task manager.

### 📦 依赖 (Imports)
- `import asyncio`
- `from collections import OrderedDict`
- `from dataclasses import dataclass`
- `from dataclasses import field`
- `from typing import Any`
- `from typing import Self`
- `import shortuuid`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from agentscope.message import TextBlock`
- `from agentscope.message import ToolResultState`
- `from agentscope.permission import PermissionContext`
- `from agentscope.permission import PermissionDecision`
- `from agentscope.permission import PermissionBehavior`
- `from agentscope.tool import ToolBase`
- `from agentscope.tool import ToolChunk`
- `from agentscope._logging import logger`

### 🏗️ 类 (Classes)
- `class BackgroundTask:`
- `class _TaskStopParams(BaseModel):`
- `class TaskStop(ToolBase):`
- `    def __init__(...):`
- `class BackgroundTaskManager:`
- `    def __init__(...):`
- `    def cancel_session_tasks(...):`

---

## 📄 agentscope/src/agentscope/app/_manager/_cancel_dispatcher.py
> **模块说明**: Single per-process dispatcher for cross-process session cancels.

### 📦 依赖 (Imports)
- `import asyncio`
- `from typing import TYPE_CHECKING`
- `from typing import Self`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class CancelDispatcher:`
- `    def __init__(...):`
- `    def _cancel_local(...):`

---

## 📄 agentscope/src/agentscope/app/_manager/_chat_run_registry.py
> **模块说明**: Per-process registry of in-flight ``ChatService.run`` asyncio tasks.

### 📦 依赖 (Imports)
- `import asyncio`
- `from typing import Coroutine`
- `from typing import Self`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class ChatRunRegistry:`
- `    def __init__(...):`
- `    def spawn(...):`
- `    def get(...):`

---

## 📄 agentscope/src/agentscope/app/_manager/_scheduler/__init__.py
> **模块说明**: The scheduler related components.

### 📦 依赖 (Imports)
- `from _scheduler_manager import SchedulerManager`

---

## 📄 agentscope/src/agentscope/app/_manager/_scheduler/_scheduler_manager.py
> **模块说明**: The cron scheduler manager class.

### 📦 依赖 (Imports)
- `import json`
- `from collections.abc import Callable`
- `from collections.abc import Coroutine`
- `from typing import Self`
- `from message import HintBlock`
- `from permission import PermissionContext`
- `from state import AgentState`
- `from tool import ToolBase`
- `from _logging import logger`
- `from _tools import ScheduleCreate`
- `from _tools import ScheduleDelete`
- `from _tools import ScheduleList`
- `from _tools import ScheduleView`
- `from message_bus import MessageBus`
- `from storage import StorageBase`
- `from storage import ScheduleRecord`
- `from storage import ChatModelConfig`
- `from storage import SessionConfig`
- `from storage import SessionSource`

### 🏗️ 类 (Classes)
- `class SchedulerManager:`
- `    def __init__(...):`
- `    def _build_trigger(...):`

---

## 📄 agentscope/src/agentscope/app/_manager/_scheduler/_tools/__init__.py
> **模块说明**: The schedule related tools.

### 📦 依赖 (Imports)
- `from _schedule_create import ScheduleCreate`
- `from _schedule_delete import ScheduleDelete`
- `from _schedule_list import ScheduleList`
- `from _schedule_view import ScheduleView`

---

## 📄 agentscope/src/agentscope/app/_manager/_scheduler/_tools/_schedule_create.py
> **模块说明**: The schedule create tool.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from typing import Any`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from message import ToolResultState`
- `from message import TextBlock`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from permission import PermissionMode`
- `from state import AgentState`
- `from tool import ToolBase`
- `from tool import ToolChunk`
- `from storage import ScheduleData`
- `from storage import ScheduleRecord`
- `from storage import ScheduleSource`
- `from storage import ChatModelConfig`

### 🏗️ 类 (Classes)
- `class _ScheduleCreateParams(BaseModel):`
- `class ScheduleCreate(ToolBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_manager/_scheduler/_tools/_schedule_delete.py
> **模块说明**: Schedule delete tool – removes a job from the scheduler and storage.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from apscheduler.jobstores.base import JobLookupError`
- `from message import ToolResultState`
- `from message import TextBlock`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from tool import ToolBase`
- `from tool import ToolChunk`
- `from message_bus import MessageBus`
- `from storage._base import StorageBase`

### 🏗️ 类 (Classes)
- `class _ScheduleDeleteParams(BaseModel):`
- `class ScheduleDelete(ToolBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_manager/_scheduler/_tools/_schedule_list.py
> **模块说明**: The tool to list the scheduled jobs in the cron scheduler manager.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from pydantic import BaseModel`
- `from message import ToolResultState`
- `from message import TextBlock`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from tool import ToolBase`
- `from tool import ToolChunk`
- `from storage import StorageBase`

### 🏗️ 类 (Classes)
- `class _ScheduleListParams(BaseModel):`
- `class ScheduleList(ToolBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_manager/_scheduler/_tools/_schedule_view.py
> **模块说明**: The schedule view tool.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from message import ToolResultState`
- `from message import TextBlock`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from tool import ToolBase`
- `from tool import ToolChunk`
- `from storage import StorageBase`

### 🏗️ 类 (Classes)
- `class _ScheduleViewParams(BaseModel):`
- `class ScheduleView(ToolBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_manager/_wakeup_dispatcher.py
> **模块说明**: Single per-process dispatcher for cross-session wake-ups.

### 📦 依赖 (Imports)
- `import asyncio`
- `from typing import TYPE_CHECKING`
- `from typing import Self`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class WakeupDispatcher:`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_router/__init__.py
> **模块说明**: App routers.

### 📦 依赖 (Imports)
- `from _agent import agent_router`
- `from _chat import chat_router`
- `from _credential import credential_router`
- `from _schedule import schedule_router`
- `from _session import session_router`
- `from _model import model_router`
- `from _workspace import workspace_router`

---

## 📄 agentscope/src/agentscope/app/_router/_agent.py
> **模块说明**: Agent router — CRUD endpoints for agent configurations.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from fastapi import APIRouter`
- `from fastapi import Depends`
- `from fastapi import HTTPException`
- `from fastapi import status`
- `from agent import ContextConfig`
- `from agent import ReActConfig`
- `from deps import get_current_user_id`
- `from deps import get_session_service`
- `from deps import get_storage`
- `from _schema import AgentSchemaResponse`
- `from _schema import ListAgentsResponse`
- `from _schema import CreateAgentRequest`
- `from _schema import CreateAgentResponse`
- `from _schema import UpdateAgentRequest`
- `from _service import SessionService`
- `from storage import StorageBase`
- `from storage import AgentData`
- `from storage import AgentRecord`

---

## 📄 agentscope/src/agentscope/app/_router/_chat.py
> **模块说明**: Chat router — fire-and-forget trigger for chat runs.

### 📦 依赖 (Imports)
- `from fastapi import APIRouter`
- `from fastapi import Depends`
- `from fastapi import HTTPException`
- `from fastapi import status`
- `from deps import get_chat_run_registry`
- `from deps import get_chat_service`
- `from deps import get_current_user_id`
- `from _schema import ChatRequest`
- `from _schema import ChatTriggerResponse`
- `from _manager import ChatRunRegistry`
- `from _service import ChatService`

---

## 📄 agentscope/src/agentscope/app/_router/_credential.py
> **模块说明**: Credential router — CRUD endpoints for API key credentials.

### 📦 依赖 (Imports)
- `from fastapi import APIRouter`
- `from fastapi import Depends`
- `from fastapi import HTTPException`
- `from fastapi import status`
- `from deps import get_current_user_id`
- `from deps import get_storage`
- `from _schema import CreateCredentialRequest`
- `from _schema import CreateCredentialResponse`
- `from _schema import ListCredentialsResponse`
- `from _schema import ListCredentialSchemasResponse`
- `from _schema import UpdateCredentialRequest`
- `from storage import StorageBase`
- `from storage import CredentialRecord`
- `from credential import CredentialFactory`

---

## 📄 agentscope/src/agentscope/app/_router/_model.py
> **模块说明**: The model router.

### 📦 依赖 (Imports)
- `from fastapi import APIRouter`
- `from fastapi import Depends`
- `from fastapi import HTTPException`
- `from fastapi import status`
- `from _schema import ListModelsResponse`
- `from _schema import ListModelsRequest`
- `from credential import CredentialFactory`

---

## 📄 agentscope/src/agentscope/app/_router/_schedule.py
> **模块说明**: Schedule router — CRUD endpoints for scheduled agent tasks.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from fastapi import APIRouter`
- `from fastapi import Depends`
- `from fastapi import HTTPException`
- `from fastapi import status`
- `from _manager import SchedulerManager`
- `from deps import get_current_user_id`
- `from deps import get_scheduler_manager`
- `from deps import get_session_service`
- `from deps import get_storage`
- `from _schema import CreateScheduleRequest`
- `from _schema import CreateScheduleResponse`
- `from _schema import ListSchedulesResponse`
- `from _schema import ScheduleSessionsResponse`
- `from _schema import UpdateScheduleRequest`
- `from _service import SessionService`
- `from storage import StorageBase`
- `from storage import ScheduleData`
- `from storage import ScheduleRecord`
- `from storage import ScheduleSource`

---

## 📄 agentscope/src/agentscope/app/_router/_schema/__init__.py
> **模块说明**: Schema models for the agent service.

### 📦 依赖 (Imports)
- `from _chat import ChatRequest`
- `from _chat import ChatTriggerResponse`
- `from _model import ListModelsResponse`
- `from _model import ListModelsRequest`
- `from _schedule import CreateScheduleRequest`
- `from _schedule import CreateScheduleResponse`
- `from _schedule import ListSchedulesResponse`
- `from _schedule import ScheduleSessionsResponse`
- `from _schedule import UpdateScheduleRequest`
- `from _agent import AgentSchemaResponse`
- `from _agent import ListAgentsResponse`
- `from _agent import CreateAgentRequest`
- `from _agent import CreateAgentResponse`
- `from _agent import UpdateAgentRequest`
- `from _credential import CreateCredentialRequest`
- `from _credential import CreateCredentialResponse`
- `from _credential import UpdateCredentialRequest`
- `from _credential import ListCredentialsResponse`
- `from _credential import ListCredentialSchemasResponse`
- `from _session import CreateSessionRequest`
- `from _session import CreateSessionResponse`
- `from _session import UpdateSessionRequest`
- `from _session import ListSessionsResponse`
- `from _session import ListMessagesResponse`
- `from _session import SessionView`
- `from _session import TeamDetailResponse`
- `from _session import TeamMemberView`

---

## 📄 agentscope/src/agentscope/app/_router/_schema/_agent.py
> **模块说明**: Request / response schemas for the agent router.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from agent import ContextConfig`
- `from agent import ReActConfig`
- `from storage import AgentRecord`

### 🏗️ 类 (Classes)
- `class CreateAgentRequest(BaseModel):`
- `class CreateAgentResponse(BaseModel):`
- `class UpdateAgentRequest(BaseModel):`
- `class ListAgentsResponse(BaseModel):`
- `class AgentSchemaResponse(BaseModel):`

---

## 📄 agentscope/src/agentscope/app/_router/_schema/_chat.py
> **模块说明**: The chat endpoint schema.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from message import Msg`
- `from event import UserConfirmResultEvent`
- `from event import ExternalExecutionResultEvent`

### 🏗️ 类 (Classes)
- `class ChatRequest(BaseModel):`
- `class ChatTriggerResponse(BaseModel):`

---

## 📄 agentscope/src/agentscope/app/_router/_schema/_credential.py
> **模块说明**: Request / response schemas for the credential router.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from storage import CredentialRecord`

### 🏗️ 类 (Classes)
- `class CreateCredentialRequest(BaseModel):`
- `class CreateCredentialResponse(BaseModel):`
- `class UpdateCredentialRequest(BaseModel):`
- `class ListCredentialsResponse(BaseModel):`
- `class ListCredentialSchemasResponse(BaseModel):`

---

## 📄 agentscope/src/agentscope/app/_router/_schema/_mcp.py
> **模块说明**: MCP schemas for API requests and responses.

### 📦 依赖 (Imports)
- `from enum import Enum`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from mcp import StdioMCPConfig`
- `from mcp import HttpMCPConfig`

### 🏗️ 类 (Classes)
- `class ConnectionScope(str, Enum):`
- `class MCPBase(BaseModel):`
- `    def validate_config(...):`
- `class MCPCreateRequest(MCPBase):`
- `class MCPUpdateRequest(BaseModel):`
- `class MCPResponse(MCPBase):`
- `class ListMCPsResponse(BaseModel):`

---

## 📄 agentscope/src/agentscope/app/_router/_schema/_model.py
> **模块说明**: The chat model configuration, used as DTO layer.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from model import ModelCard`

### 🏗️ 类 (Classes)
- `class ListModelsResponse(BaseModel):`
- `class ListModelsRequest(BaseModel):`

---

## 📄 agentscope/src/agentscope/app/_router/_schema/_schedule.py
> **模块说明**: Request / response schemas for the schedule router.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from storage import ScheduleRecord`
- `from storage import SessionRecord`
- `from storage import ChatModelConfig`
- `from permission import PermissionMode`

### 🏗️ 类 (Classes)
- `class CreateScheduleRequest(BaseModel):`
- `class CreateScheduleResponse(BaseModel):`
- `class UpdateScheduleRequest(BaseModel):`
- `class ListSchedulesResponse(BaseModel):`
- `class ScheduleSessionsResponse(BaseModel):`

---

## 📄 agentscope/src/agentscope/app/_router/_schema/_session.py
> **模块说明**: Request / response schemas for the session router.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from permission import PermissionMode`
- `from storage import AgentRecord`
- `from storage import ChatModelConfig`
- `from storage import SessionRecord`
- `from storage import TeamRecord`

### 🏗️ 类 (Classes)
- `class TeamMemberView(BaseModel):`
- `class TeamDetailResponse(BaseModel):`
- `class CreateSessionRequest(BaseModel):`
- `class CreateSessionResponse(BaseModel):`
- `class UpdateSessionRequest(BaseModel):`
- `class SessionView(BaseModel):`
- `class ListSessionsResponse(BaseModel):`
- `class ListMessagesResponse(BaseModel):`

---

## 📄 agentscope/src/agentscope/app/_router/_session.py
> **模块说明**: Session router — create, list, update, delete, stream, and get messages.

### 📦 依赖 (Imports)
- `import asyncio`
- `import json`
- `import uuid`
- `from typing import AsyncGenerator`
- `from fastapi import APIRouter`
- `from fastapi import Depends`
- `from fastapi import HTTPException`
- `from fastapi import Query`
- `from fastapi import status`
- `from fastapi.responses import StreamingResponse`
- `from deps import get_current_user_id`
- `from deps import get_message_bus`
- `from deps import get_session_service`
- `from deps import get_storage`
- `from _schema import CreateSessionRequest`
- `from _schema import CreateSessionResponse`
- `from _schema import ListMessagesResponse`
- `from _schema import ListSessionsResponse`
- `from _schema import SessionView`
- `from _schema import TeamDetailResponse`
- `from _schema import TeamMemberView`
- `from _schema import UpdateSessionRequest`
- `from message_bus import MessageBus`
- `from _service import SessionService`
- `from storage import AgentRecord`
- `from storage import ChatModelConfig`
- `from storage import SessionConfig`
- `from storage import SessionRecord`
- `from storage import StorageBase`
- `from storage import TeamRecord`

---

## 📄 agentscope/src/agentscope/app/_router/_workspace.py
> **模块说明**: Workspace router — manage MCP clients and skills on a workspace.

### 📦 依赖 (Imports)
- `from fastapi import APIRouter`
- `from fastapi import Depends`
- `from fastapi import HTTPException`
- `from fastapi import Query`
- `from fastapi import status`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from deps import get_current_user_id`
- `from deps import get_storage`
- `from deps import get_workspace_manager`
- `from workspace_manager import WorkspaceManagerBase`
- `from storage import StorageBase`
- `from mcp import MCPClient`
- `from skill import Skill`
- `from workspace import WorkspaceBase`

### 🏗️ 类 (Classes)
- `class AddSkillRequest(BaseModel):`
- `class ToolInfo(BaseModel):`
- `class MCPClientStatus(MCPClient):`

---

## 📄 agentscope/src/agentscope/app/_service/__init__.py
> **模块说明**: Service layer for the AgentScope app.

### 📦 依赖 (Imports)
- `from _chat import ChatService`
- `from _model import get_model`
- `from _session import SessionService`
- `from _toolkit import get_toolkit`

---

## 📄 agentscope/src/agentscope/app/_service/_chat.py
> **模块说明**: Chat service encapsulating agent execution + persistence logic.

### 📦 依赖 (Imports)
- `from fastapi import HTTPException`
- `from message_bus import MessageBus`
- `from storage import StorageBase`
- `from _manager import BackgroundTaskManager`
- `from _manager import SchedulerManager`
- `from workspace_manager import WorkspaceManagerBase`
- `from middleware import InboxMiddleware`
- `from middleware import StateChangeMiddleware`
- `from middleware import ToolOffloadMiddleware`
- `from _types import AgentMiddlewareFactory`
- `from _types import AgentToolFactory`
- `from _types import SubAgentTemplate`
- `from _model import get_model`
- `from _toolkit import get_toolkit`
- `from _logging import logger`
- `from agent import Agent`
- `from agent import ModelConfig`
- `from event import ReplyStartEvent`
- `from event import UserConfirmResultEvent`
- `from event import ExternalExecutionResultEvent`
- `from message import AssistantMsg`
- `from message import Msg`
- `from message import ToolCallState`
- `from permission import AdditionalWorkingDirectory`

### 🏗️ 类 (Classes)
- `class ChatService:`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_service/_model.py
> **模块说明**: Model service: builds a ChatModelBase from stored credential + config.

### 📦 依赖 (Imports)
- `from fastapi import HTTPException`
- `from fastapi import status`
- `from storage import StorageBase`
- `from storage import ChatModelConfig`
- `from credential import CredentialFactory`
- `from model import ChatModelBase`

---

## 📄 agentscope/src/agentscope/app/_service/_session.py
> **模块说明**: Cross-resource session lifecycle service.

### 📦 依赖 (Imports)
- `import asyncio`
- `from message_bus import MessageBus`
- `from storage import StorageBase`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class SessionService:`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_service/_toolkit.py
> **模块说明**: Toolkit assembly for an (agent, session) pair.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from _manager import BackgroundTaskManager`
- `from _manager import SchedulerManager`
- `from message_bus import MessageBus`
- `from _tools import AgentCreate`
- `from _tools import TeamCreate`
- `from _tools import TeamDelete`
- `from _tools import TeamSay`
- `from _types import AgentToolFactory`
- `from _types import SubAgentTemplate`
- `from storage import AgentRecord`
- `from storage import SessionRecord`
- `from storage import StorageBase`
- `from tool import TaskCreate`
- `from tool import TaskGet`
- `from tool import TaskList`
- `from tool import TaskUpdate`
- `from tool import Toolkit`
- `from tool import ToolGroup`
- `from workspace import WorkspaceBase`

---

## 📄 agentscope/src/agentscope/app/_tools/__init__.py
> **模块说明**: Framework-builtin tools wired into team-participating agents.

### 📦 依赖 (Imports)
- `from _agent_create import AgentCreate`
- `from _agent_create import DEFAULT_SUB_AGENT_TEMPLATE`
- `from _team_create import TeamCreate`
- `from _team_delete import TeamDelete`
- `from _team_say import TeamSay`

---

## 📄 agentscope/src/agentscope/app/_tools/_agent_create.py
> **模块说明**: The AgentCreate tool — spawns a worker into the current team.

### 📦 依赖 (Imports)
- `from __future__ import annotations`
- `import copy`
- `import json`
- `from typing import TYPE_CHECKING`
- `from pydantic import Field`
- `from _team_tool_base import _TeamToolBase`
- `from _types import SubAgentTemplate`
- `from storage import AgentData`
- `from storage import AgentRecord`
- `from storage import SessionConfig`
- `from message import HintBlock`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from state import AgentState`
- `from tool import ToolChunk`
- `from tool import ParamsBase`

### 🏗️ 类 (Classes)
- `class _AgentCreateParams(ParamsBase):`
- `class AgentCreate(_TeamToolBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_tools/_team_create.py
> **模块说明**: The TeamCreate tool — establishes a new team led by the current session.

### 📦 依赖 (Imports)
- `from pydantic import Field`
- `from _team_tool_base import _TeamToolBase`
- `from storage import TeamData`
- `from storage import TeamRecord`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from tool import ToolChunk`
- `from tool import ParamsBase`

### 🏗️ 类 (Classes)
- `class _TeamCreateParams(ParamsBase):`
- `class TeamCreate(_TeamToolBase):`

---

## 📄 agentscope/src/agentscope/app/_tools/_team_delete.py
> **模块说明**: The TeamDelete tool — dissolves the team led by the current session.

### 📦 依赖 (Imports)
- `from _team_tool_base import _TeamToolBase`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from tool import ToolChunk`
- `from tool import ParamsBase`

### 🏗️ 类 (Classes)
- `class _TeamDeleteParams(ParamsBase):`
- `class TeamDelete(_TeamToolBase):`

---

## 📄 agentscope/src/agentscope/app/_tools/_team_say.py
> **模块说明**: The TeamSay tool — sends a message to one or all team members.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from pydantic import Field`
- `from _team_tool_base import _TeamToolBase`
- `from message import HintBlock`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from tool import ToolChunk`
- `from tool import ParamsBase`

### 🏗️ 类 (Classes)
- `class _TeamSayParams(ParamsBase):`
- `class TeamSay(_TeamToolBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_tools/_team_tool_base.py
> **模块说明**: Base class shared by the team tools.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from typing import TYPE_CHECKING`
- `from permission import PermissionBehavior`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from tool import ToolBase`

### 🏗️ 类 (Classes)
- `class _TeamToolBase(ToolBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/_types.py
> **模块说明**: Shared type aliases for the agentscope app layer.

### 📦 依赖 (Imports)
- `from collections.abc import Awaitable`
- `from collections.abc import Callable`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from agent import ContextConfig`
- `from agent import ReActConfig`
- `from middleware import MiddlewareBase`
- `from permission import PermissionContext`
- `from state import TaskContext`
- `from tool import ToolBase`

### 🏗️ 类 (Classes)
- `class SubAgentTemplate(BaseModel):`

---

## 📄 agentscope/src/agentscope/app/deps.py
> **模块说明**: Shared FastAPI dependencies for the agentscope app.

### 📦 依赖 (Imports)
- `from fastapi import Header`
- `from fastapi import HTTPException`
- `from fastapi import Request`
- `from fastapi import status`
- `from workspace_manager import WorkspaceManagerBase`
- `from _manager import BackgroundTaskManager`
- `from _manager import ChatRunRegistry`
- `from _manager import SchedulerManager`
- `from _service import ChatService`
- `from _service import SessionService`
- `from _types import AgentMiddlewareFactory`
- `from _types import AgentToolFactory`
- `from message_bus import MessageBus`
- `from storage import StorageBase`

---

## 📄 agentscope/src/agentscope/app/message_bus/__init__.py
> **模块说明**: The message bus module — live transport for cross-session messages.

### 📦 依赖 (Imports)
- `from _base import MessageBus`
- `from _redis_message_bus import RedisMessageBus`

---

## 📄 agentscope/src/agentscope/app/message_bus/_base.py
> **模块说明**: The message bus abstract base class.

### 📦 依赖 (Imports)
- `from abc import ABC`
- `from abc import abstractmethod`
- `from collections.abc import AsyncGenerator`
- `from contextlib import asynccontextmanager`
- `from typing import Any`
- `from typing import Callable`
- `from typing import Self`

### 🏗️ 类 (Classes)
- `class MessageBus(ABC):`

---

## 📄 agentscope/src/agentscope/app/message_bus/_redis_message_bus.py
> **模块说明**: The Redis-backed message bus implementation.

### 📦 依赖 (Imports)
- `import asyncio`
- `import json`
- `import uuid`
- `from collections.abc import AsyncGenerator`
- `from contextlib import asynccontextmanager`
- `from typing import Any`
- `from typing import Callable`
- `from typing import Self`
- `from typing import TYPE_CHECKING`
- `from _base import MessageBus`

### 🏗️ 类 (Classes)
- `class RedisMessageBus(MessageBus):`
- `    def __init__(...):`
- `    def get_client(...):`
- `    def _exclusive_start(...):`

---

## 📄 agentscope/src/agentscope/app/middleware/__init__.py
> **模块说明**: The middlewares module.

### 📦 依赖 (Imports)
- `from _inbox_middleware import InboxMiddleware`
- `from _protocol import ProtocolMiddlewareBase`
- `from _protocol import AGUIProtocolMiddleware`
- `from _state_change_middleware import StateChangeMiddleware`
- `from _tool_offload_middleware import ToolOffloadMiddleware`

---

## 📄 agentscope/src/agentscope/app/middleware/_inbox_middleware.py
> **模块说明**: Generic middleware that drains the message bus inbox before reasoning.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import Callable`
- `from message_bus import MessageBus`
- `from _logging import logger`
- `from agent import Agent`
- `from event import HintBlockEvent`
- `from message import AssistantMsg`
- `from message import HintBlock`
- `from middleware import MiddlewareBase`

### 🏗️ 类 (Classes)
- `class InboxMiddleware(MiddlewareBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/middleware/_protocol/__init__.py
> **模块说明**: The middleware used for agent protocol.

### 📦 依赖 (Imports)
- `from _base import ProtocolMiddlewareBase`
- `from _agui import AGUIProtocolMiddleware`

---

## 📄 agentscope/src/agentscope/app/middleware/_protocol/_agui.py
> **模块说明**: The AGUI middleware class.

### 📦 依赖 (Imports)
- `from typing import TYPE_CHECKING`
- `from typing import Any`
- `from starlette.types import ASGIApp`
- `from _base import ProtocolMiddlewareBase`
- `from event import AgentEvent`
- `from event import DataBlockDeltaEvent`
- `from event import DataBlockEndEvent`
- `from event import DataBlockStartEvent`
- `from event import ExceedMaxItersEvent`
- `from event import ExternalExecutionResultEvent`
- `from event import ModelCallEndEvent`
- `from event import ModelCallStartEvent`
- `from event import ReplyEndEvent`
- `from event import ReplyStartEvent`
- `from event import RequireExternalExecutionEvent`
- `from event import RequireUserConfirmEvent`
- `from event import TextBlockDeltaEvent`
- `from event import TextBlockEndEvent`
- `from event import TextBlockStartEvent`
- `from event import ThinkingBlockDeltaEvent`
- `from event import ThinkingBlockEndEvent`
- `from event import ThinkingBlockStartEvent`
- `from event import ToolCallDeltaEvent`
- `from event import ToolCallEndEvent`
- `from event import ToolCallStartEvent`
- `from event import ToolResultDataDeltaEvent`
- `from event import ToolResultEndEvent`
- `from event import ToolResultStartEvent`
- `from event import ToolResultTextDeltaEvent`
- `from event import UserConfirmResultEvent`

### 🏗️ 类 (Classes)
- `class AGUIProtocolMiddleware(ProtocolMiddlewareBase):`
- `    def __init__(...):`
- `    def _convert_to_protocol(...):`
- `    def _to_agui_event(...):`

---

## 📄 agentscope/src/agentscope/app/middleware/_protocol/_base.py
> **模块说明**: Protocol middleware base class for converting AgentEvent stream to

### 📦 依赖 (Imports)
- `import json`
- `from abc import ABC`
- `from abc import abstractmethod`
- `from typing import AsyncGenerator`
- `from typing import Callable`
- `from fastapi import Request`
- `from fastapi import Response`
- `from fastapi.responses import StreamingResponse`
- `from starlette.middleware.base import BaseHTTPMiddleware`
- `from starlette.types import ASGIApp`
- `from agentscope.event import AgentEvent`

### 🏗️ 类 (Classes)
- `class ProtocolMiddlewareBase(BaseHTTPMiddleware, ABC):`
- `    def __init__(...):`
- `    def _deserialize_event(...):`
- `    def _convert_to_protocol(...):`

---

## 📄 agentscope/src/agentscope/app/middleware/_state_change_middleware.py
> **模块说明**: Middleware that detects agent state / team changes after each tool

### 📦 依赖 (Imports)
- `import hashlib`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import Callable`
- `from message_bus import MessageBus`
- `from event import CustomEvent`
- `from middleware import MiddlewareBase`

### 🏗️ 类 (Classes)
- `class StateChangeMiddleware(MiddlewareBase):`
- `    def __init__(...):`
- `    def _state_hash(...):`

---

## 📄 agentscope/src/agentscope/app/middleware/_tool_offload_middleware.py
> **模块说明**: Middleware that offloads long-running tool calls to background tasks.

### 📦 依赖 (Imports)
- `import asyncio`
- `import json`
- `from copy import deepcopy`
- `from typing import AsyncGenerator`
- `from typing import Callable`
- `from _manager import BackgroundTaskManager`
- `from middleware import MiddlewareBase`
- `from tool import ToolChunk`
- `from tool import ToolResponse`
- `from message import DataBlock`
- `from message import HintBlock`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from agent import Agent`
- `from message_bus import MessageBus`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class ToolOffloadMiddleware(MiddlewareBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/app/storage/__init__.py
> **模块说明**: The storage module in agentscope.

### 📦 依赖 (Imports)
- `from _base import StorageBase`
- `from _redis_storage import RedisStorage`
- `from _model import AgentData`
- `from _model import AgentRecord`
- `from _model import CredentialRecord`
- `from _model import ScheduleData`
- `from _model import ScheduleRecord`
- `from _model import ScheduleSource`
- `from _model import SessionConfig`
- `from _model import SessionRecord`
- `from _model import SessionSource`
- `from _model import ChatModelConfig`
- `from _model import TeamData`
- `from _model import TeamRecord`
- `from _model import UserRecord`

---

## 📄 agentscope/src/agentscope/app/storage/_base.py
> **模块说明**: The storage base class.

### 📦 依赖 (Imports)
- `from abc import ABC`
- `from abc import abstractmethod`
- `from typing import Any`
- `from typing import Self`
- `from _model import AgentRecord`
- `from _model import CredentialRecord`
- `from _model import ScheduleRecord`
- `from _model import SessionRecord`
- `from _model import SessionConfig`
- `from _model import SessionSource`
- `from _model import TeamRecord`
- `from credential import CredentialBase`
- `from message import Msg`
- `from state import AgentState`

### 🏗️ 类 (Classes)
- `class StorageBase(ABC):`

---

## 📄 agentscope/src/agentscope/app/storage/_model/__init__.py
> **模块说明**: Storage models for persisted resources.

### 📦 依赖 (Imports)
- `from _agent import AgentRecord`
- `from _agent import AgentData`
- `from _credential import CredentialRecord`
- `from _schedule import ScheduleData`
- `from _schedule import ScheduleRecord`
- `from _schedule import ScheduleSource`
- `from _session import SessionRecord`
- `from _session import SessionConfig`
- `from _session import ChatModelConfig`
- `from _session import SessionSource`
- `from _team import TeamRecord`
- `from _team import TeamData`
- `from _user import UserRecord`

---

## 📄 agentscope/src/agentscope/app/storage/_model/_agent.py
> **模块说明**: The agent storage class.

### 📦 依赖 (Imports)
- `import uuid`
- `from typing import Literal`
- `from pydantic import Field`
- `from pydantic import BaseModel`
- `from _base import _RecordBase`
- `from agent import ContextConfig`
- `from agent import ReActConfig`

### 🏗️ 类 (Classes)
- `class AgentData(BaseModel):`
- `class AgentRecord(_RecordBase):`

---

## 📄 agentscope/src/agentscope/app/storage/_model/_base.py
> **模块说明**: The base attributes used in storage.

### 📦 依赖 (Imports)
- `import uuid`
- `from datetime import datetime`
- `from pydantic import BaseModel`
- `from pydantic import Field`

### 🏗️ 类 (Classes)
- `class _RecordBase(BaseModel):`

---

## 📄 agentscope/src/agentscope/app/storage/_model/_credential.py
> **模块说明**: The credential record.

### 📦 依赖 (Imports)
- `import uuid`
- `from pydantic import Field`
- `from _base import _RecordBase`

### 🏗️ 类 (Classes)
- `class CredentialRecord(_RecordBase):`

---

## 📄 agentscope/src/agentscope/app/storage/_model/_schedule.py
> **模块说明**: The schedule storage model.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from enum import Enum`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import _RecordBase`
- `from _session import ChatModelConfig`
- `from permission import PermissionMode`

### 🏗️ 类 (Classes)
- `class ScheduleSource(str, Enum):`
- `class ScheduleData(BaseModel):`
- `class ScheduleRecord(_RecordBase):`

### ⚡ 函数 (Functions)
- `def _get_local_timezone(...):`

---

## 📄 agentscope/src/agentscope/app/storage/_model/_session.py
> **模块说明**: The session data class for storage.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from enum import Enum`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import _RecordBase`
- `from state import AgentState`

### 🏗️ 类 (Classes)
- `class SessionSource(str, Enum):`
- `class ChatModelConfig(BaseModel):`
- `class SessionConfig(BaseModel):`
- `class SessionRecord(_RecordBase):`

---

## 📄 agentscope/src/agentscope/app/storage/_model/_team.py
> **模块说明**: The team storage class.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import _RecordBase`

### 🏗️ 类 (Classes)
- `class TeamData(BaseModel):`
- `class TeamRecord(_RecordBase):`

---

## 📄 agentscope/src/agentscope/app/storage/_model/_user.py
> **模块说明**: The user record for storage.

### 📦 依赖 (Imports)
- `from _base import _RecordBase`

### 🏗️ 类 (Classes)
- `class UserRecord(_RecordBase):`

---

## 📄 agentscope/src/agentscope/app/storage/_redis_storage.py
> **模块说明**: The Redis storage implementation.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from typing import Any`
- `from typing import TYPE_CHECKING`
- `from typing import Self`
- `from pydantic import BaseModel`
- `from _base import StorageBase`
- `from _model import AgentRecord`
- `from _model import CredentialRecord`
- `from _model import ScheduleRecord`
- `from _model import SessionRecord`
- `from _model import SessionConfig`
- `from _model import SessionSource`
- `from _model import TeamRecord`
- `from _utils import _dump_with_secrets`
- `from credential import CredentialBase`
- `from message import Msg`
- `from state import AgentState`

### 🏗️ 类 (Classes)
- `class RedisStorage(StorageBase):`
- `    def __init__(...):`
- `    def _key(...):`
- `    def get_client(...):`
- `    def _message_key(...):`

---

## 📄 agentscope/src/agentscope/app/storage/_utils.py
> **模块说明**: The utils for storage.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import SecretStr`

### ⚡ 函数 (Functions)
- `def _dump_with_secrets(...):`

---

## 📄 agentscope/src/agentscope/app/workspace_manager/__init__.py
> **模块说明**: The workspace manager classes, responsible for managing the resources

### 📦 依赖 (Imports)
- `from _base import WorkspaceManagerBase`
- `from _local_workspace_manager import LocalWorkspaceManager`
- `from _docker_workspace_manager import DockerWorkspaceManager`
- `from _e2b_workspace_manager import E2BWorkspaceManager`

---

## 📄 agentscope/src/agentscope/app/workspace_manager/_base.py
> **模块说明**: Workspace manager implementations.

### 📦 依赖 (Imports)
- `from abc import ABC`
- `from abc import abstractmethod`
- `from typing import Self`
- `from workspace import WorkspaceBase`

### 🏗️ 类 (Classes)
- `class WorkspaceManagerBase(ABC):`

---

## 📄 agentscope/src/agentscope/app/workspace_manager/_docker_workspace_manager.py
> **模块说明**: DockerWorkspaceManager — lifecycle manager for :class:`DockerWorkspace`.

### 📦 依赖 (Imports)
- `import asyncio`
- `import os`
- `import time`
- `from typing import Self`
- `from agentscope._logging import logger`
- `from agentscope.mcp import MCPClient`
- `from agentscope.workspace._docker import DockerWorkspace`
- `from agentscope.workspace._docker._make_dockerfile import DEFAULT_BASE_IMAGE`
- `from agentscope.workspace._docker._make_dockerfile import DEFAULT_GATEWAY_PORT`
- `from _base import WorkspaceManagerBase`

### 🏗️ 类 (Classes)
- `class DockerWorkspaceManager(WorkspaceManagerBase):`
- `    def __init__(...):`
- `    def _workdir_for(...):`

---

## 📄 agentscope/src/agentscope/app/workspace_manager/_e2b_workspace_manager.py
> **模块说明**: E2BWorkspaceManager — lifecycle manager for :class:`E2BWorkspace`.

### 📦 依赖 (Imports)
- `import asyncio`
- `import time`
- `from typing import Self`
- `from agentscope._logging import logger`
- `from agentscope.mcp import MCPClient`
- `from agentscope.workspace import E2BWorkspace`
- `from agentscope.workspace._e2b._bootstrap import DEFAULT_GATEWAY_PORT`
- `from agentscope.workspace._e2b._bootstrap import DEFAULT_TEMPLATE`
- `from agentscope.workspace._e2b._bootstrap import DEFAULT_TIMEOUT`
- `from _base import WorkspaceManagerBase`

### 🏗️ 类 (Classes)
- `class E2BWorkspaceManager(WorkspaceManagerBase):`
- `    def __init__(...):`
- `    def _metadata_for(...):`

---

## 📄 agentscope/src/agentscope/app/workspace_manager/_local_workspace_manager.py
> **模块说明**: The local workspace manager.

### 📦 依赖 (Imports)
- `import asyncio`
- `import os`
- `import time`
- `from _logging import logger`
- `from workspace import LocalWorkspace`
- `from _base import WorkspaceManagerBase`

### 🏗️ 类 (Classes)
- `class LocalWorkspaceManager(WorkspaceManagerBase):`
- `    def __init__(...):`
- `    def _pop_expired(...):`

---

## 📄 agentscope/src/agentscope/credential/__init__.py
> **模块说明**: The credential module.

### 📦 依赖 (Imports)
- `from _base import CredentialBase`
- `from _anthropic import AnthropicCredential`
- `from _dashscope import DashScopeCredential`
- `from _deepseek import DeepSeekCredential`
- `from _gemini import GeminiCredential`
- `from _moonshot import MoonshotCredential`
- `from _ollama import OllamaCredential`
- `from _openai import OpenAICredential`
- `from _xai import XAICredential`
- `from _factory import CredentialFactory`

---

## 📄 agentscope/src/agentscope/credential/_anthropic.py
> **模块说明**: The Anthropic credential.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from pydantic import Field`
- `from pydantic import SecretStr`
- `from pydantic import ConfigDict`
- `from _base import CredentialBase`

### 🏗️ 类 (Classes)
- `class AnthropicCredential(CredentialBase):`
- `    def get_chat_model_class(...):`

---

## 📄 agentscope/src/agentscope/credential/_base.py
> **模块说明**: The credential base class.

### 📦 依赖 (Imports)
- `import uuid`
- `from typing import TYPE_CHECKING`
- `from typing import Type`
- `from pydantic import BaseModel`
- `from pydantic import Field`

### 🏗️ 类 (Classes)
- `class CredentialBase(BaseModel):`
- `    def get_chat_model_class(...):`
- `    def list_models(...):`

---

## 📄 agentscope/src/agentscope/credential/_dashscope.py
> **模块说明**: The DashScope credential.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from pydantic import ConfigDict`
- `from pydantic import Field`
- `from pydantic import SecretStr`
- `from _base import CredentialBase`

### 🏗️ 类 (Classes)
- `class DashScopeCredential(CredentialBase):`
- `    def get_chat_model_class(...):`

---

## 📄 agentscope/src/agentscope/credential/_deepseek.py
> **模块说明**: The DeepSeek credential.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from pydantic import ConfigDict`
- `from pydantic import Field`
- `from pydantic import SecretStr`
- `from _base import CredentialBase`

### 🏗️ 类 (Classes)
- `class DeepSeekCredential(CredentialBase):`
- `    def get_chat_model_class(...):`

---

## 📄 agentscope/src/agentscope/credential/_factory.py
> **模块说明**: The credential factory class.

### 📦 依赖 (Imports)
- `from typing import Annotated`
- `from typing import Type`
- `from typing import Union`
- `from typing import get_args`
- `from typing import get_type_hints`
- `from pydantic import TypeAdapter`
- `from pydantic import Field`
- `from _anthropic import AnthropicCredential`
- `from _dashscope import DashScopeCredential`
- `from _deepseek import DeepSeekCredential`
- `from _gemini import GeminiCredential`
- `from _moonshot import MoonshotCredential`
- `from _ollama import OllamaCredential`
- `from _openai import OpenAICredential`
- `from _xai import XAICredential`
- `from _base import CredentialBase`

### 🏗️ 类 (Classes)
- `class CredentialFactory:`
- `    def _get_adapter(...):`
- `    def register_credential(...):`
- `    def from_dict(...):`
- `    def get_credential_class(...):`
- `    def list_schemas(...):`

---

## 📄 agentscope/src/agentscope/credential/_gemini.py
> **模块说明**: The Google Gemini credential.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from pydantic import ConfigDict`
- `from pydantic import Field`
- `from pydantic import SecretStr`
- `from _base import CredentialBase`

### 🏗️ 类 (Classes)
- `class GeminiCredential(CredentialBase):`
- `    def get_chat_model_class(...):`

---

## 📄 agentscope/src/agentscope/credential/_kimi.py

---

## 📄 agentscope/src/agentscope/credential/_moonshot.py
> **模块说明**: The Moonshot AI credential.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from pydantic import Field`
- `from pydantic import SecretStr`
- `from _base import CredentialBase`

### 🏗️ 类 (Classes)
- `class MoonshotCredential(CredentialBase):`
- `    def get_chat_model_class(...):`

---

## 📄 agentscope/src/agentscope/credential/_ollama.py
> **模块说明**: The Ollama credential.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from pydantic import ConfigDict`
- `from pydantic import Field`
- `from _base import CredentialBase`

### 🏗️ 类 (Classes)
- `class OllamaCredential(CredentialBase):`
- `    def get_chat_model_class(...):`

---

## 📄 agentscope/src/agentscope/credential/_openai.py
> **模块说明**: The OpenAI credential.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from pydantic import ConfigDict`
- `from pydantic import Field`
- `from pydantic import SecretStr`
- `from _base import CredentialBase`

### 🏗️ 类 (Classes)
- `class OpenAICredential(CredentialBase):`
- `    def get_chat_model_class(...):`

---

## 📄 agentscope/src/agentscope/credential/_xai.py
> **模块说明**: The xAI credential.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from pydantic import ConfigDict`
- `from pydantic import Field`
- `from pydantic import SecretStr`
- `from _base import CredentialBase`

### 🏗️ 类 (Classes)
- `class XAICredential(CredentialBase):`
- `    def get_chat_model_class(...):`

---

## 📄 agentscope/src/agentscope/embedding/__init__.py
> **模块说明**: The embedding module in agentscope.

### 📦 依赖 (Imports)
- `from _embedding_base import EmbeddingModelBase`
- `from _embedding_usage import EmbeddingUsage`
- `from _embedding_response import EmbeddingResponse`
- `from _dashscope_embedding import DashScopeTextEmbedding`
- `from _dashscope_multimodal_embedding import DashScopeMultiModalEmbedding`
- `from _openai_embedding import OpenAITextEmbedding`
- `from _gemini_embedding import GeminiTextEmbedding`
- `from _ollama_embedding import OllamaTextEmbedding`
- `from _cache_base import EmbeddingCacheBase`
- `from _file_cache import FileEmbeddingCache`

---

## 📄 agentscope/src/agentscope/embedding/_cache_base.py
> **模块说明**: The embedding cache base class.

### 📦 依赖 (Imports)
- `from abc import abstractmethod`
- `from typing import List`
- `from typing import Any`
- `from types import JSONSerializableObject`
- `from types import Embedding`

### 🏗️ 类 (Classes)
- `class EmbeddingCacheBase:`

---

## 📄 agentscope/src/agentscope/embedding/_dashscope_embedding.py
> **模块说明**: The dashscope embedding module in agentscope.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from typing import Any`
- `from typing import List`
- `from typing import Literal`
- `from _cache_base import EmbeddingCacheBase`
- `from _embedding_response import EmbeddingResponse`
- `from _embedding_usage import EmbeddingUsage`
- `from _embedding_base import EmbeddingModelBase`
- `from _logging import logger`
- `from message import TextBlock`

### 🏗️ 类 (Classes)
- `class DashScopeTextEmbedding(EmbeddingModelBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/embedding/_dashscope_multimodal_embedding.py
> **模块说明**: The dashscope multimodal embedding model in agentscope.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from typing import Any`
- `from typing import Literal`
- `from _cache_base import EmbeddingCacheBase`
- `from _embedding_response import EmbeddingResponse`
- `from _embedding_usage import EmbeddingUsage`
- `from _embedding_base import EmbeddingModelBase`
- `from message import DataBlock`
- `from message import TextBlock`

### 🏗️ 类 (Classes)
- `class DashScopeMultiModalEmbedding(EmbeddingModelBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/embedding/_embedding_base.py
> **模块说明**: The embedding model base class.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from _embedding_response import EmbeddingResponse`

### 🏗️ 类 (Classes)
- `class EmbeddingModelBase:`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/embedding/_embedding_response.py
> **模块说明**: The embedding response class.

### 📦 依赖 (Imports)
- `from dataclasses import dataclass`
- `from dataclasses import field`
- `from typing import Literal`
- `from typing import List`
- `from _embedding_usage import EmbeddingUsage`
- `from _utils._common import _get_timestamp`
- `from _utils._mixin import DictMixin`
- `from types import Embedding`

### 🏗️ 类 (Classes)
- `class EmbeddingResponse(DictMixin):`

---

## 📄 agentscope/src/agentscope/embedding/_embedding_usage.py
> **模块说明**: The embedding usage class in agentscope.

### 📦 依赖 (Imports)
- `from dataclasses import dataclass`
- `from dataclasses import field`
- `from typing import Literal`
- `from _utils._mixin import DictMixin`

### 🏗️ 类 (Classes)
- `class EmbeddingUsage(DictMixin):`

---

## 📄 agentscope/src/agentscope/embedding/_file_cache.py
> **模块说明**: A file embedding cache implementation for storing and retrieving

### 📦 依赖 (Imports)
- `import hashlib`
- `import json`
- `import os`
- `from typing import Any`
- `from typing import List`
- `import numpy`
- `from _cache_base import EmbeddingCacheBase`
- `from _logging import logger`
- `from types import Embedding`
- `from types import JSONSerializableObject`

### 🏗️ 类 (Classes)
- `class FileEmbeddingCache(EmbeddingCacheBase):`
- `    def __init__(...):`
- `    def cache_dir(...):`
- `    def _get_cache_size(...):`
- `    def _get_filename(...):`

---

## 📄 agentscope/src/agentscope/embedding/_gemini_embedding.py
> **模块说明**: The gemini text embedding model class.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from typing import Any`
- `from typing import List`
- `from _embedding_response import EmbeddingResponse`
- `from _embedding_usage import EmbeddingUsage`
- `from _cache_base import EmbeddingCacheBase`
- `from _embedding_base import EmbeddingModelBase`
- `from message import TextBlock`

### 🏗️ 类 (Classes)
- `class GeminiTextEmbedding(EmbeddingModelBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/embedding/_ollama_embedding.py
> **模块说明**: The ollama text embedding model class.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from typing import List`
- `from typing import Any`
- `from _embedding_response import EmbeddingResponse`
- `from _embedding_usage import EmbeddingUsage`
- `from _cache_base import EmbeddingCacheBase`
- `from embedding import EmbeddingModelBase`
- `from message import TextBlock`

### 🏗️ 类 (Classes)
- `class OllamaTextEmbedding(EmbeddingModelBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/embedding/_openai_embedding.py
> **模块说明**: The OpenAI text embedding model class.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from typing import Any`
- `from typing import List`
- `from _embedding_response import EmbeddingResponse`
- `from _embedding_usage import EmbeddingUsage`
- `from _cache_base import EmbeddingCacheBase`
- `from _embedding_base import EmbeddingModelBase`
- `from message import TextBlock`

### 🏗️ 类 (Classes)
- `class OpenAITextEmbedding(EmbeddingModelBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/event/__init__.py
> **模块说明**: The event module of agentscope.

### 📦 依赖 (Imports)
- `from _event import EventType`
- `from _event import EventBase`
- `from _event import ReplyStartEvent`
- `from _event import ReplyEndEvent`
- `from _event import ModelCallStartEvent`
- `from _event import ModelCallEndEvent`
- `from _event import TextBlockStartEvent`
- `from _event import TextBlockDeltaEvent`
- `from _event import TextBlockEndEvent`
- `from _event import DataBlockStartEvent`
- `from _event import DataBlockDeltaEvent`
- `from _event import DataBlockEndEvent`
- `from _event import ThinkingBlockStartEvent`
- `from _event import ThinkingBlockDeltaEvent`
- `from _event import ThinkingBlockEndEvent`
- `from _event import HintBlockEvent`
- `from _event import ToolCallStartEvent`
- `from _event import ToolCallDeltaEvent`
- `from _event import ToolCallEndEvent`
- `from _event import ToolResultStartEvent`
- `from _event import ToolResultTextDeltaEvent`
- `from _event import ToolResultDataDeltaEvent`
- `from _event import ToolResultEndEvent`
- `from _event import ExceedMaxItersEvent`
- `from _event import RequireUserConfirmEvent`
- `from _event import RequireExternalExecutionEvent`
- `from _event import UserConfirmResultEvent`
- `from _event import ExternalExecutionResultEvent`
- `from _event import CustomEvent`
- `from _event import AgentEvent`
- `from _event import ConfirmResult`

---

## 📄 agentscope/src/agentscope/event/_event.py
> **模块说明**: Event types for agent execution.

### 📦 依赖 (Imports)
- `import uuid`
- `from datetime import datetime`
- `from enum import StrEnum`
- `from typing import Any`
- `from typing import Dict`
- `from typing import Literal`
- `from typing import List`
- `from typing import TypeAlias`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from pydantic import ConfigDict`
- `from message import DataBlock`
- `from message import TextBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`
- `from message import ToolResultState`
- `from permission import PermissionRule`

### 🏗️ 类 (Classes)
- `class EventType(StrEnum):`
- `class EventBase(BaseModel):`
- `class ReplyStartEvent(EventBase):`
- `class ReplyEndEvent(EventBase):`
- `class ModelCallStartEvent(EventBase):`
- `class ModelCallEndEvent(EventBase):`
- `class TextBlockStartEvent(EventBase):`
- `class TextBlockDeltaEvent(EventBase):`
- `class TextBlockEndEvent(EventBase):`
- `class DataBlockStartEvent(EventBase):`
- `class DataBlockDeltaEvent(EventBase):`
- `class DataBlockEndEvent(EventBase):`
- `class ThinkingBlockStartEvent(EventBase):`
- `class ThinkingBlockDeltaEvent(EventBase):`
- `class ThinkingBlockEndEvent(EventBase):`
- `class HintBlockEvent(EventBase):`
- `class ToolCallStartEvent(EventBase):`
- `class ToolCallDeltaEvent(EventBase):`
- `class ToolCallEndEvent(EventBase):`
- `class ToolResultStartEvent(EventBase):`
- `class ToolResultTextDeltaEvent(EventBase):`
- `class ToolResultDataDeltaEvent(EventBase):`
- `class ToolResultEndEvent(EventBase):`
- `class ExceedMaxItersEvent(EventBase):`
- `class RequireUserConfirmEvent(EventBase):`
- `class RequireExternalExecutionEvent(EventBase):`
- `class ConfirmResult(BaseModel):`
- `class UserConfirmResultEvent(EventBase):`
- `class ExternalExecutionResultEvent(EventBase):`
- `class CustomEvent(EventBase):`

---

## 📄 agentscope/src/agentscope/exception/__init__.py
> **模块说明**: The exception module in agentscope.

### 📦 依赖 (Imports)
- `from _base import AgentOrientedException`
- `from _base import DeveloperOrientedException`
- `from _tool import ToolInterruptedError`
- `from _tool import ToolNotFoundError`
- `from _tool import ToolJSONDecodeError`
- `from _tool import ToolGroupInactiveError`

---

## 📄 agentscope/src/agentscope/exception/_base.py
> **模块说明**: The base exception class in agentscope.

### 🏗️ 类 (Classes)
- `class AgentOrientedException(Exception):`
- `    def __init__(...):`
- `    def __str__(...):`
- `class DeveloperOrientedException(Exception):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/exception/_tool.py
> **模块说明**: The tool-related exceptions in agentscope.

### 📦 依赖 (Imports)
- `from _base import AgentOrientedException`

### 🏗️ 类 (Classes)
- `class ToolNotFoundError(AgentOrientedException):`
- `class ToolInterruptedError(AgentOrientedException):`
- `class ToolJSONDecodeError(AgentOrientedException):`
- `class ToolGroupInactiveError(AgentOrientedException):`

---

## 📄 agentscope/src/agentscope/formatter/__init__.py
> **模块说明**: The formatter module in agentscope.

### 📦 依赖 (Imports)
- `from _formatter_base import FormatterBase`
- `from _dashscope_formatter import DashScopeChatFormatter`
- `from _dashscope_formatter import DashScopeMultiAgentFormatter`
- `from _anthropic_formatter import AnthropicChatFormatter`
- `from _anthropic_formatter import AnthropicMultiAgentFormatter`
- `from _openai_formatter import OpenAIChatFormatter`
- `from _openai_formatter import OpenAIMultiAgentFormatter`
- `from _gemini_formatter import GeminiChatFormatter`
- `from _gemini_formatter import GeminiMultiAgentFormatter`
- `from _ollama_formatter import OllamaChatFormatter`
- `from _ollama_formatter import OllamaMultiAgentFormatter`
- `from _deepseek_formatter import DeepSeekChatFormatter`
- `from _deepseek_formatter import DeepSeekMultiAgentFormatter`
- `from _openai_response_formatter import OpenAIResponseFormatter`
- `from _openai_response_formatter import OpenAIResponseMultiAgentFormatter`
- `from _moonshot_formatter import MoonshotChatFormatter`
- `from _moonshot_formatter import MoonshotMultiAgentFormatter`
- `from _xai_formatter import XAIChatFormatter`
- `from _xai_formatter import XAIMultiAgentFormatter`

---

## 📄 agentscope/src/agentscope/formatter/_anthropic_formatter.py
> **模块说明**: The Anthropic formatter module.

### 📦 依赖 (Imports)
- `import base64`
- `import fnmatch`
- `import json`
- `from abc import ABC`
- `from typing import Any`
- `import requests`
- `from pydantic import Field`
- `from _formatter_base import FormatterBase`
- `from _logging import logger`
- `from message import Msg`
- `from message import TextBlock`
- `from message import ThinkingBlock`
- `from message import HintBlock`
- `from message import DataBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`
- `from message import URLSource`
- `from message import Base64Source`

### 🏗️ 类 (Classes)
- `class _AnthropicFormatterBase(FormatterBase, ABC):`
- `    def _format_anthropic_data_block(...):`
- `    def _format_image_source(...):`
- `class AnthropicChatFormatter(_AnthropicFormatterBase):`
- `class AnthropicMultiAgentFormatter(_AnthropicFormatterBase):`

---

## 📄 agentscope/src/agentscope/formatter/_dashscope_formatter.py
> **模块说明**: The DashScope formatter module (OpenAI-compatible format).

### 📦 依赖 (Imports)
- `import base64`
- `from typing import Any`
- `from fnmatch import fnmatch`
- `from abc import ABC`
- `from pydantic import Field`
- `from _formatter_base import FormatterBase`
- `from _logging import logger`
- `from message import Msg`
- `from message import TextBlock`
- `from message import ThinkingBlock`
- `from message import ToolResultBlock`
- `from message import URLSource`
- `from message import DataBlock`
- `from message import ToolCallBlock`
- `from message import Base64Source`
- `from message import HintBlock`

### 🏗️ 类 (Classes)
- `class _DashScopeFormatterBase(FormatterBase, ABC):`
- `    def supported_input_media_types(...):`
- `    def supports_thinking_input(...):`
- `    def _format_dashscope_data_block(...):`
- `    def _format_image_source(...):`
- `    def _format_video_source(...):`
- `    def _format_audio_source(...):`
- `class DashScopeChatFormatter(_DashScopeFormatterBase):`
- `class DashScopeMultiAgentFormatter(_DashScopeFormatterBase):`

---

## 📄 agentscope/src/agentscope/formatter/_deepseek_formatter.py
> **模块说明**: The DeepSeek formatter module.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from pydantic import Field`
- `from _formatter_base import FormatterBase`
- `from _logging import logger`
- `from message import Msg`
- `from message import TextBlock`
- `from message import DataBlock`
- `from message import ThinkingBlock`
- `from message import HintBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`

### 🏗️ 类 (Classes)
- `class DeepSeekChatFormatter(FormatterBase):`
- `class DeepSeekMultiAgentFormatter(FormatterBase):`

---

## 📄 agentscope/src/agentscope/formatter/_formatter_base.py
> **模块说明**: The formatter module.

### 📦 依赖 (Imports)
- `import base64`
- `import mimetypes`
- `import tempfile`
- `from abc import abstractmethod`
- `from fnmatch import fnmatch`
- `from typing import Any`
- `from typing import List`
- `from typing import AsyncGenerator`
- `import shortuuid`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from message import Msg`
- `from message import DataBlock`
- `from message import TextBlock`
- `from message import URLSource`
- `from message import Base64Source`

### 🏗️ 类 (Classes)
- `class FormatterBase(BaseModel):`
- `    def supported_input_media_types(...):`
- `    def assert_list_of_msgs(...):`
- `    def convert_tool_result_to_string(...):`

---

## 📄 agentscope/src/agentscope/formatter/_gemini_formatter.py
> **模块说明**: Google Gemini API formatter in agentscope.

### 📦 依赖 (Imports)
- `import base64`
- `import fnmatch`
- `import json`
- `from abc import ABC`
- `from typing import Any`
- `import requests`
- `from pydantic import Field`
- `from _formatter_base import FormatterBase`
- `from _logging import logger`
- `from message import Msg`
- `from message import TextBlock`
- `from message import ThinkingBlock`
- `from message import HintBlock`
- `from message import DataBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`
- `from message import URLSource`
- `from message import Base64Source`

### 🏗️ 类 (Classes)
- `class _GeminiFormatterBase(FormatterBase, ABC):`
- `    def _format_gemini_data_block(...):`
- `    def _format_media_source(...):`
- `class GeminiChatFormatter(_GeminiFormatterBase):`
- `class GeminiMultiAgentFormatter(_GeminiFormatterBase):`

---

## 📄 agentscope/src/agentscope/formatter/_moonshot_formatter.py
> **模块说明**: The Moonshot AI formatter for agentscope.

### 📦 依赖 (Imports)
- `import base64`
- `from typing import Any`
- `import requests`
- `from pydantic import Field`
- `from _openai_formatter import _OpenAIFormatterBase`
- `from _logging import logger`
- `from message import Msg`
- `from message import URLSource`
- `from message import Base64Source`
- `from message import TextBlock`
- `from message import DataBlock`
- `from message import ThinkingBlock`
- `from message import HintBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`

### 🏗️ 类 (Classes)
- `class MoonshotChatFormatter(_OpenAIFormatterBase):`
- `    def _format_image_source(...):`
- `class MoonshotMultiAgentFormatter(_OpenAIFormatterBase):`
- `    def _format_image_source(...):`

### ⚡ 函数 (Functions)
- `def _moonshot_format_image_source(...):`

---

## 📄 agentscope/src/agentscope/formatter/_ollama_formatter.py
> **模块说明**: The Ollama formatter module.

### 📦 依赖 (Imports)
- `import base64`
- `import fnmatch`
- `import json`
- `from abc import ABC`
- `from typing import Any`
- `import requests`
- `from pydantic import Field`
- `from _formatter_base import FormatterBase`
- `from _logging import logger`
- `from message import Msg`
- `from message import TextBlock`
- `from message import HintBlock`
- `from message import DataBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`
- `from message import ThinkingBlock`
- `from message import URLSource`
- `from message import Base64Source`

### 🏗️ 类 (Classes)
- `class _OllamaFormatterBase(FormatterBase, ABC):`
- `    def _format_ollama_data_block(...):`
- `    def _format_image_source(...):`
- `class OllamaChatFormatter(_OllamaFormatterBase):`
- `class OllamaMultiAgentFormatter(_OllamaFormatterBase):`

---

## 📄 agentscope/src/agentscope/formatter/_openai_formatter.py
> **模块说明**: The OpenAI formatter for agentscope.

### 📦 依赖 (Imports)
- `import base64`
- `from abc import ABC`
- `from fnmatch import fnmatch`
- `from typing import Any`
- `from urllib.parse import urlparse`
- `import requests`
- `from pydantic import Field`
- `from _formatter_base import FormatterBase`
- `from _logging import logger`
- `from message import Msg`
- `from message import URLSource`
- `from message import TextBlock`
- `from message import DataBlock`
- `from message import Base64Source`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`
- `from message import HintBlock`
- `from message import ThinkingBlock`

### 🏗️ 类 (Classes)
- `class _OpenAIFormatterBase(FormatterBase, ABC):`
- `    def _format_openai_data_block(...):`
- `    def _format_image_source(...):`
- `    def _format_audio_source(...):`
- `class OpenAIChatFormatter(_OpenAIFormatterBase):`
- `class OpenAIMultiAgentFormatter(_OpenAIFormatterBase):`

---

## 📄 agentscope/src/agentscope/formatter/_openai_response_formatter.py
> **模块说明**: Formatters for the OpenAI Responses API.

### 📦 依赖 (Imports)
- `from abc import ABC`
- `from typing import Any`
- `from pydantic import Field`
- `from _openai_formatter import _OpenAIFormatterBase`
- `from _logging import logger`
- `from message import Msg`
- `from message import TextBlock`
- `from message import DataBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`
- `from message import HintBlock`
- `from message import ThinkingBlock`

### 🏗️ 类 (Classes)
- `class _OpenAIResponseFormatterBase(_OpenAIFormatterBase, ABC):`
- `    def _format_response_data_block(...):`
- `class OpenAIResponseFormatter(_OpenAIResponseFormatterBase):`
- `class OpenAIResponseMultiAgentFormatter(_OpenAIResponseFormatterBase):`

---

## 📄 agentscope/src/agentscope/formatter/_xai_formatter.py
> **模块说明**: The xAI formatter module.

### 📦 依赖 (Imports)
- `import base64`
- `from typing import Any`
- `from typing import List`
- `from pydantic import Field`
- `from _formatter_base import FormatterBase`
- `from _logging import logger`
- `from message import Msg`
- `from message import TextBlock`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`
- `from message import DataBlock`
- `from message import URLSource`
- `from message import Base64Source`
- `from message import HintBlock`

### 🏗️ 类 (Classes)
- `class XAIChatFormatter(FormatterBase):`
- `    def _xai_user_args_from_blocks(...):`
- `    def _extract_result_text(...):`
- `class XAIMultiAgentFormatter(FormatterBase):`
- `    def _build_history_text(...):`

---

## 📄 agentscope/src/agentscope/mcp/__init__.py
> **模块说明**: The MCP module in AgentScope, that provides fine-grained control over

### 📦 依赖 (Imports)
- `from _config import StdioMCPConfig`
- `from _config import HttpMCPConfig`
- `from _mcp_client import MCPClient`

---

## 📄 agentscope/src/agentscope/mcp/_config.py
> **模块说明**: The MCP configurations.

### 📦 依赖 (Imports)
- `from pathlib import Path`
- `from typing import Literal`
- `from pydantic import BaseModel`
- `from pydantic import Field`

### 🏗️ 类 (Classes)
- `class StdioMCPConfig(BaseModel):`
- `class HttpMCPConfig(BaseModel):`

---

## 📄 agentscope/src/agentscope/mcp/_mcp_client.py
> **模块说明**: Unified MCP client implementation for AgentScope.

### 📦 依赖 (Imports)
- `import re`
- `from contextlib import AsyncExitStack`
- `from contextlib import _AsyncGeneratorContextManager`
- `from typing import Any`
- `from typing import TYPE_CHECKING`
- `import httpx`
- `import mcp.types`
- `from mcp import ClientSession`
- `from mcp import stdio_client`
- `from mcp import StdioServerParameters`
- `from mcp.client.sse import sse_client`
- `from mcp.client.streamable_http import streamable_http_client`
- `from pydantic import Field`
- `from pydantic import BaseModel`
- `from pydantic import PrivateAttr`
- `from _config import StdioMCPConfig`
- `from _config import HttpMCPConfig`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class MCPClient(BaseModel):`
- `    def is_connected(...):`
- `    def model_post_init(...):`
- `    def _initialize_client(...):`
- `    def _create_http_client(...):`
- `    def _get_client_gen(...):`
- `    def _validate_connection(...):`

---

## 📄 agentscope/src/agentscope/message/__init__.py
> **模块说明**: The message module in agentscope.

### 📦 依赖 (Imports)
- `from _block import ContentBlock`
- `from _block import ContentBlockTypes`
- `from _block import TextBlock`
- `from _block import ThinkingBlock`
- `from _block import HintBlock`
- `from _block import ToolCallBlock`
- `from _block import ToolCallState`
- `from _block import ToolResultBlock`
- `from _block import ToolResultState`
- `from _block import DataBlock`
- `from _block import Base64Source`
- `from _block import URLSource`
- `from _base import Msg`
- `from _base import UserMsg`
- `from _base import AssistantMsg`
- `from _base import SystemMsg`
- `from _base import Usage`

---

## 📄 agentscope/src/agentscope/message/_base.py
> **模块说明**: The message class in agentscope.

### 📦 依赖 (Imports)
- `import base64`
- `import uuid`
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import List`
- `from typing import overload`
- `from typing import Sequence`
- `from typing import Self`
- `from typing import TYPE_CHECKING`
- `from typing import Any`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from pydantic import model_validator`
- `from _block import TextBlock`
- `from _block import ThinkingBlock`
- `from _block import HintBlock`
- `from _block import DataBlock`
- `from _block import Base64Source`
- `from _block import URLSource`
- `from _block import ToolCallBlock`
- `from _block import ToolCallState`
- `from _block import ToolResultBlock`
- `from _block import ToolResultState`
- `from _block import ContentBlock`
- `from _block import ContentBlockTypes`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class Usage(BaseModel):`
- `class Msg(BaseModel):`
- `    def validate_role_content(...):`
- `    def has_content_blocks(...):`
- `    def get_text_content(...):`
- `    def get_content_blocks(...):`
- `    def get_content_blocks(...):`
- `    def get_content_blocks(...):`
- `    def get_content_blocks(...):`
- `    def get_content_blocks(...):`
- `    def get_content_blocks(...):`
- `    def get_content_blocks(...):`
- `    def get_content_blocks(...):`
- `    def _find_block(...):`
- `    def append_event(...):`

### ⚡ 函数 (Functions)
- `def _assert_user_content_blocks(...):`
- `def _assert_system_content_blocks(...):`
- `def _to_blocks(...):`
- `def UserMsg(...):`
- `def AssistantMsg(...):`
- `def SystemMsg(...):`

---

## 📄 agentscope/src/agentscope/message/_block.py
> **模块说明**: The content blocks of messages.

### 📦 依赖 (Imports)
- `import uuid`
- `from enum import StrEnum`
- `from typing import Literal`
- `from typing import List`
- `from typing import TypeAlias`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from pydantic import AnyUrl`
- `from pydantic import field_serializer`
- `from pydantic import ConfigDict`
- `from permission import PermissionRule`

### 🏗️ 类 (Classes)
- `class TextBlock(BaseModel):`
- `class ThinkingBlock(BaseModel):`
- `class Base64Source(BaseModel):`
- `class URLSource(BaseModel):`
- `    def serialize_url(...):`
- `class DataBlock(BaseModel):`
- `class HintBlock(BaseModel):`
- `class ToolCallState(StrEnum):`
- `class ToolCallBlock(BaseModel):`
- `class ToolResultState(StrEnum):`
- `class ToolResultBlock(BaseModel):`

---

## 📄 agentscope/src/agentscope/middleware/__init__.py
> **模块说明**: Middleware system for AgentScope agents.

### 📦 依赖 (Imports)
- `from _base import MiddlewareBase`
- `from _tracing import TracingMiddleware`

---

## 📄 agentscope/src/agentscope/middleware/_base.py
> **模块说明**: Base middleware class for AgentScope middleware system.

### 📦 依赖 (Imports)
- `from typing import AsyncGenerator`
- `from typing import Awaitable`
- `from typing import Callable`
- `from typing import TYPE_CHECKING`
- `from tool import ToolBase`

### 🏗️ 类 (Classes)
- `class MiddlewareBase:`
- `    def is_implemented(...):`

---

## 📄 agentscope/src/agentscope/middleware/_tracing/__init__.py
> **模块说明**: The tracing interface class in agentscope.

### 📦 依赖 (Imports)
- `from _trace import TracingMiddleware`

---

## 📄 agentscope/src/agentscope/middleware/_tracing/_attributes.py
> **模块说明**: The tracing types class in agentscope.

### 📦 依赖 (Imports)
- `from opentelemetry.semconv._incubating.attributes import gen_ai_attributes`

### 🏗️ 类 (Classes)
- `class SpanAttributes:`
- `class OperationNameValues:`
- `class ProviderNameValues:`

---

## 📄 agentscope/src/agentscope/middleware/_tracing/_converter.py
> **模块说明**: Convert ContentBlock to OpenTelemetry GenAI part format.

### 📦 依赖 (Imports)
- `import json`
- `from typing import Any`
- `from typing import Dict`
- `from message import ContentBlock`
- `from message import TextBlock`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import ToolResultBlock`
- `from message import DataBlock`
- `from message import Base64Source`
- `from message import URLSource`
- `from _utils import _serialize_to_str`

### ⚡ 函数 (Functions)
- `def _get_modality(...):`
- `def _convert_media_block(...):`
- `def _convert_block_to_part(...):`

---

## 📄 agentscope/src/agentscope/middleware/_tracing/_extractor.py
> **模块说明**: Extract attributes from AgentScope components for OpenTelemetry tracing.

### 📦 依赖 (Imports)
- `import inspect`
- `from typing import Any`
- `from typing import Dict`
- `from typing import TYPE_CHECKING`
- `from message import Msg`
- `from message import ToolCallBlock`
- `from _attributes import SpanAttributes`
- `from _attributes import OperationNameValues`
- `from _attributes import ProviderNameValues`
- `from _converter import _convert_block_to_part`
- `from _utils import _serialize_to_str`
- `from model import ChatResponse`
- `from model import ChatModelBase`
- `from event import ExternalExecutionResultEvent`
- `from event import UserConfirmResultEvent`

### ⚡ 函数 (Functions)
- `def _get_common_attributes(...):`
- `def _get_provider_name(...):`
- `def _get_tool_definitions(...):`
- `def _get_llm_request_attributes(...):`
- `def _get_llm_span_name(...):`
- `def _get_llm_output_messages(...):`
- `def _get_llm_response_attributes(...):`
- `def _get_agent_messages(...):`
- `def _get_agent_request_attributes(...):`
- `def _get_agent_span_name(...):`
- `def _get_agent_response_attributes(...):`
- `def _get_tool_request_attributes(...):`
- `def _get_tool_span_name(...):`
- `def _get_tool_response_attributes(...):`

---

## 📄 agentscope/src/agentscope/middleware/_tracing/_setup.py
> **模块说明**: The tracing interface class in agentscope.

### 📦 依赖 (Imports)
- `from typing import TYPE_CHECKING`

### ⚡ 函数 (Functions)
- `def _get_tracer(...):`

---

## 📄 agentscope/src/agentscope/middleware/_tracing/_trace.py
> **模块说明**: TracingMiddleware and supporting utilities for OpenTelemetry tracing.

### 📦 依赖 (Imports)
- `import json`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import Callable`
- `from typing import Awaitable`
- `from typing import Union`
- `from typing import TypeVar`
- `from typing import TYPE_CHECKING`
- `import aioitertools`
- `from opentelemetry import trace`
- `from opentelemetry.trace import StatusCode`
- `from _base import MiddlewareBase`
- `from event import ExternalExecutionResultEvent`
- `from event import RequireExternalExecutionEvent`
- `from event import RequireUserConfirmEvent`
- `from event import ReplyStartEvent`
- `from message import Msg`
- `from message import ToolCallBlock`
- `from model import ChatModelBase`
- `from _attributes import SpanAttributes`
- `from _attributes import OperationNameValues`
- `from _extractor import _get_common_attributes`
- `from _extractor import _get_agent_request_attributes`
- `from _extractor import _get_agent_span_name`
- `from _extractor import _get_agent_response_attributes`
- `from _extractor import _get_llm_request_attributes`
- `from _extractor import _get_llm_span_name`
- `from _extractor import _get_llm_response_attributes`
- `from _extractor import _get_tool_request_attributes`
- `from _extractor import _get_tool_span_name`
- `from _extractor import _get_tool_response_attributes`
- `from _setup import _get_tracer`
- `from _utils import _serialize_to_str`

### 🏗️ 类 (Classes)
- `class TracingMiddleware(MiddlewareBase):`

### ⚡ 函数 (Functions)
- `def _check_tracing_enabled(...):`
- `def _set_span_success_status(...):`
- `def _set_span_error_status(...):`

---

## 📄 agentscope/src/agentscope/middleware/_tracing/_utils.py
> **模块说明**: Serialize objects to JSON string.

### 📦 依赖 (Imports)
- `import datetime`
- `import enum`
- `import inspect`
- `import json`
- `from dataclasses import is_dataclass`
- `from typing import Any`
- `from pydantic import BaseModel`
- `from message import Msg`

### ⚡ 函数 (Functions)
- `def _to_serializable(...):`
- `def _serialize_to_str(...):`

---

## 📄 agentscope/src/agentscope/model/__init__.py
> **模块说明**: The model module.

### 📦 依赖 (Imports)
- `from _base import ChatModelBase`
- `from _model_card import ModelCard`
- `from _model_response import ChatResponse`
- `from _model_response import StructuredResponse`
- `from _model_usage import ChatUsage`
- `from _anthropic import AnthropicChatModel`
- `from _dashscope import DashScopeChatModel`
- `from _deepseek import DeepSeekChatModel`
- `from _gemini import GeminiChatModel`
- `from _ollama import OllamaChatModel`
- `from _openai_chat import OpenAIChatModel`
- `from _xai import XAIChatModel`
- `from _moonshot import MoonshotChatModel`
- `from _openai_response import OpenAIResponseModel`

---

## 📄 agentscope/src/agentscope/model/_anthropic/__init__.py
> **模块说明**: The Anthropic LLM API modules.

### 📦 依赖 (Imports)
- `from _model import AnthropicCredential`
- `from _model import AnthropicChatModel`

---

## 📄 agentscope/src/agentscope/model/_anthropic/_model.py
> **模块说明**: The Anthropic chat model implementation.

### 📦 依赖 (Imports)
- `from collections import OrderedDict`
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import TYPE_CHECKING`
- `from typing import List`
- `from typing import Type`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import ChatModelBase`
- `from _base import _TOOL_CHOICE_LITERAL_MODES`
- `from _model_response import ChatResponse`
- `from _model_response import StructuredResponse`
- `from _model_usage import ChatUsage`
- `from credential import AnthropicCredential`
- `from formatter import FormatterBase`
- `from formatter import AnthropicChatFormatter`
- `from message import Msg`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import TextBlock`
- `from tool import ToolChoice`

### 🏗️ 类 (Classes)
- `class AnthropicChatModel(ChatModelBase):`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def _format_tools(...):`

---

## 📄 agentscope/src/agentscope/model/_base.py
> **模块说明**: The base class for the chat models.

### 📦 依赖 (Imports)
- `import asyncio`
- `import inspect`
- `import json`
- `from abc import abstractmethod`
- `from copy import deepcopy`
- `from pathlib import Path`
- `from typing import Type`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `import jsonschema`
- `from pydantic import BaseModel`
- `from _model_response import StructuredResponse`
- `from _model_response import ChatResponse`
- `from _model_card import ModelCard`
- `from _logging import logger`
- `from _utils._common import _json_loads_with_repair`
- `from credential import CredentialBase`
- `from message import Msg`
- `from message import TextBlock`
- `from message import UserMsg`
- `from message import ToolCallBlock`
- `from message import ThinkingBlock`
- `from message import ToolResultBlock`
- `from message import DataBlock`
- `from message import URLSource`
- `from message import Base64Source`
- `from message import HintBlock`
- `from tool import ToolChoice`

### 🏗️ 类 (Classes)
- `class ChatModelBase:`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def list_models(...):`
- `    def _validate_tool_choice(...):`

---

## 📄 agentscope/src/agentscope/model/_dashscope/__init__.py
> **模块说明**: The DashScope API modules.

### 📦 依赖 (Imports)
- `from _model import DashScopeChatModel`
- `from _model import DashScopeCredential`

---

## 📄 agentscope/src/agentscope/model/_dashscope/_model.py
> **模块说明**: The DashScope chat model class (OpenAI-compatible implementation).

### 📦 依赖 (Imports)
- `import base64`
- `import io`
- `import uuid`
- `import warnings`
- `import wave`
- `from collections import OrderedDict`
- `from datetime import datetime`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import List`
- `from typing import Literal`
- `from typing import Type`
- `from typing import TYPE_CHECKING`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import ChatModelBase`
- `from _base import _TOOL_CHOICE_LITERAL_MODES`
- `from _model_response import ChatResponse`
- `from _model_response import StructuredResponse`
- `from _model_usage import ChatUsage`
- `from _utils._audio import _build_streaming_wav_header`
- `from credential import DashScopeCredential`
- `from formatter import FormatterBase`
- `from formatter import DashScopeChatFormatter`
- `from message import Msg`
- `from message import TextBlock`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import DataBlock`
- `from message import Base64Source`
- `from tool import ToolChoice`

### 🏗️ 类 (Classes)
- `class DashScopeChatModel(ChatModelBase):`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def _parse_completion_response(...):`
- `    def _format_tools(...):`

---

## 📄 agentscope/src/agentscope/model/_deepseek/__init__.py
> **模块说明**: The DeepSeek LLM API modules.

### 📦 依赖 (Imports)
- `from _model import DeepSeekCredential`
- `from _model import DeepSeekChatModel`

---

## 📄 agentscope/src/agentscope/model/_deepseek/_model.py
> **模块说明**: The DeepSeek chat model implementation.

### 📦 依赖 (Imports)
- `from collections import OrderedDict`
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import TYPE_CHECKING`
- `from typing import List`
- `from typing import Type`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import ChatModelBase`
- `from _base import _TOOL_CHOICE_LITERAL_MODES`
- `from _model_response import ChatResponse`
- `from _model_response import StructuredResponse`
- `from _model_usage import ChatUsage`
- `from credential import DeepSeekCredential`
- `from formatter import FormatterBase`
- `from formatter import DeepSeekChatFormatter`
- `from message import Msg`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import TextBlock`
- `from tool import ToolChoice`

### 🏗️ 类 (Classes)
- `class DeepSeekChatModel(ChatModelBase):`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def _parse_completion_response(...):`
- `    def _format_tools(...):`

---

## 📄 agentscope/src/agentscope/model/_gemini/__init__.py
> **模块说明**: The Google Gemini LLM API modules.

### 📦 依赖 (Imports)
- `from _model import GeminiCredential`
- `from _model import GeminiChatModel`

---

## 📄 agentscope/src/agentscope/model/_gemini/_model.py
> **模块说明**: The Google Gemini chat model implementation.

### 📦 依赖 (Imports)
- `import base64`
- `import copy`
- `import json`
- `import uuid`
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import TYPE_CHECKING`
- `from typing import List`
- `from typing import Type`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import ChatModelBase`
- `from _base import _TOOL_CHOICE_LITERAL_MODES`
- `from _model_response import ChatResponse`
- `from _model_usage import ChatUsage`
- `from credential import GeminiCredential`
- `from formatter import FormatterBase`
- `from formatter import GeminiChatFormatter`
- `from message import Msg`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import TextBlock`
- `from tool import ToolChoice`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class GeminiChatModel(ChatModelBase):`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def _parse_completion_response(...):`
- `    def _extract_usage(...):`
- `    def _format_tools(...):`

### ⚡ 函数 (Functions)
- `def _flatten_json_schema(...):`

---

## 📄 agentscope/src/agentscope/model/_model_card.py
> **模块说明**: The model card class.

### 📦 依赖 (Imports)
- `import copy`
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import Self`
- `from typing import Type`
- `import yaml`
- `from pydantic import BaseModel`
- `from pydantic import Field`

### 🏗️ 类 (Classes)
- `class ModelCard(BaseModel):`
- `    def from_yaml(...):`

---

## 📄 agentscope/src/agentscope/model/_model_response.py
> **模块说明**: The model response module.

### 📦 依赖 (Imports)
- `import uuid`
- `from dataclasses import dataclass`
- `from dataclasses import field`
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import Sequence`
- `from _model_usage import ChatUsage`
- `from _utils._mixin import DictMixin`
- `from message import TextBlock`
- `from message import ToolCallBlock`
- `from message import ThinkingBlock`
- `from message import DataBlock`
- `from types import JSONSerializableObject`

### 🏗️ 类 (Classes)
- `class ChatResponse(DictMixin):`
- `class StructuredResponse:`

---

## 📄 agentscope/src/agentscope/model/_model_usage.py
> **模块说明**: The model usage class in agentscope.

### 📦 依赖 (Imports)
- `from dataclasses import dataclass`
- `from dataclasses import field`
- `from typing import Any`
- `from typing import Literal`
- `from _utils._mixin import DictMixin`

### 🏗️ 类 (Classes)
- `class ChatUsage(DictMixin):`

---

## 📄 agentscope/src/agentscope/model/_moonshot/__init__.py
> **模块说明**: The Moonshot AI LLM API modules.

### 📦 依赖 (Imports)
- `from _model import MoonshotChatModel`

---

## 📄 agentscope/src/agentscope/model/_moonshot/_model.py
> **模块说明**: The Moonshot AI chat model implementation.

### 📦 依赖 (Imports)
- `from collections import OrderedDict`
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import TYPE_CHECKING`
- `from typing import List`
- `from typing import Type`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import ChatModelBase`
- `from _base import _TOOL_CHOICE_LITERAL_MODES`
- `from _model_response import ChatResponse`
- `from _model_response import StructuredResponse`
- `from _model_usage import ChatUsage`
- `from credential import MoonshotCredential`
- `from formatter import FormatterBase`
- `from formatter import MoonshotChatFormatter`
- `from message import Msg`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import TextBlock`
- `from tool import ToolChoice`

### 🏗️ 类 (Classes)
- `class MoonshotChatModel(ChatModelBase):`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def _parse_completion_response(...):`
- `    def _format_tools(...):`

---

## 📄 agentscope/src/agentscope/model/_ollama/__init__.py
> **模块说明**: The Ollama LLM API modules.

### 📦 依赖 (Imports)
- `from _model import OllamaCredential`
- `from _model import OllamaChatModel`

---

## 📄 agentscope/src/agentscope/model/_ollama/_model.py
> **模块说明**: The Ollama chat model implementation.

### 📦 依赖 (Imports)
- `import json`
- `import uuid`
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import TYPE_CHECKING`
- `from typing import List`
- `from typing import Type`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import ChatModelBase`
- `from _model_response import ChatResponse`
- `from _model_usage import ChatUsage`
- `from credential import OllamaCredential`
- `from formatter import FormatterBase`
- `from formatter import OllamaChatFormatter`
- `from message import Msg`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import TextBlock`
- `from tool import ToolChoice`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class OllamaChatModel(ChatModelBase):`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def _format_tools(...):`

---

## 📄 agentscope/src/agentscope/model/_openai_chat/__init__.py
> **模块说明**: The OpenAI Chat Completions API modules.

### 📦 依赖 (Imports)
- `from _model import OpenAIChatModel`

---

## 📄 agentscope/src/agentscope/model/_openai_chat/_model.py
> **模块说明**: The OpenAI Chat Completions model implementation.

### 📦 依赖 (Imports)
- `import warnings`
- `import base64`
- `import io`
- `import uuid`
- `import wave`
- `from collections import OrderedDict`
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import TYPE_CHECKING`
- `from typing import List`
- `from typing import Type`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import ChatModelBase`
- `from _base import _TOOL_CHOICE_LITERAL_MODES`
- `from _model_response import ChatResponse`
- `from _model_response import StructuredResponse`
- `from _model_usage import ChatUsage`
- `from _utils._audio import _build_streaming_wav_header`
- `from credential import OpenAICredential`
- `from formatter import FormatterBase`
- `from formatter import OpenAIChatFormatter`
- `from message import Msg`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import TextBlock`
- `from message import DataBlock`
- `from message import Base64Source`
- `from tool import ToolChoice`

### 🏗️ 类 (Classes)
- `class OpenAIChatModel(ChatModelBase):`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def _parse_completion_response(...):`
- `    def _format_tools(...):`

---

## 📄 agentscope/src/agentscope/model/_openai_response/__init__.py
> **模块说明**: The OpenAI Responses API modules.

### 📦 依赖 (Imports)
- `from _model import OpenAIResponseModel`

---

## 📄 agentscope/src/agentscope/model/_openai_response/_model.py
> **模块说明**: The OpenAI Responses API chat model implementation.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from typing import Literal`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import List`
- `from typing import TYPE_CHECKING`
- `from typing import Type`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import ChatModelBase`
- `from _base import _TOOL_CHOICE_LITERAL_MODES`
- `from _model_response import ChatResponse`
- `from _model_usage import ChatUsage`
- `from credential import OpenAICredential`
- `from formatter import FormatterBase`
- `from formatter import OpenAIResponseFormatter`
- `from message import Msg`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from message import TextBlock`
- `from tool import ToolChoice`

### 🏗️ 类 (Classes)
- `class OpenAIResponseModel(ChatModelBase):`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def _parse_completion_response(...):`
- `    def _format_tools(...):`

---

## 📄 agentscope/src/agentscope/model/_xai/__init__.py
> **模块说明**: The xAI LLM API modules.

### 📦 依赖 (Imports)
- `from _model import XAICredential`
- `from _model import XAIChatModel`

---

## 📄 agentscope/src/agentscope/model/_xai/_model.py
> **模块说明**: The xAI chat model implementation using the official xai_sdk.

### 📦 依赖 (Imports)
- `from datetime import datetime`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import List`
- `from typing import Literal`
- `from typing import TYPE_CHECKING`
- `from typing import Type`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _base import ChatModelBase`
- `from _base import _TOOL_CHOICE_LITERAL_MODES`
- `from _model_response import ChatResponse`
- `from _model_usage import ChatUsage`
- `from credential import XAICredential`
- `from formatter import XAIChatFormatter`
- `from message import Msg`
- `from message import TextBlock`
- `from message import ThinkingBlock`
- `from message import ToolCallBlock`
- `from tool import ToolChoice`

### 🏗️ 类 (Classes)
- `class XAIChatModel(ChatModelBase):`
- `    def __init__(...):`
- `    def _get_retryable_exceptions(...):`
- `    def _format_tools(...):`
- `    def _parse_completion_response(...):`

---

## 📄 agentscope/src/agentscope/permission/__init__.py
> **模块说明**: The tool permission related types and functions.

### 📦 依赖 (Imports)
- `from _context import PermissionContext`
- `from _context import AdditionalWorkingDirectory`
- `from _decision import PermissionDecision`
- `from _engine import PermissionEngine`
- `from _rule import PermissionRule`
- `from _types import PermissionMode`
- `from _types import PermissionBehavior`

---

## 📄 agentscope/src/agentscope/permission/_context.py
> **模块说明**: The permission context module.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _rule import PermissionRule`
- `from _types import PermissionMode`

### 🏗️ 类 (Classes)
- `class AdditionalWorkingDirectory(BaseModel):`
- `class PermissionContext(BaseModel):`

---

## 📄 agentscope/src/agentscope/permission/_decision.py
> **模块说明**: The permission decision result.

### 📦 依赖 (Imports)
- `from dataclasses import dataclass`
- `from typing import Any`
- `from _rule import PermissionRule`
- `from _types import PermissionBehavior`

### 🏗️ 类 (Classes)
- `class PermissionDecision:`

---

## 📄 agentscope/src/agentscope/permission/_engine.py
> **模块说明**: The permission engine for checking and enforcing permission rules.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from typing import List`
- `from typing import TYPE_CHECKING`
- `from _context import PermissionContext`
- `from _rule import PermissionRule`
- `from _decision import PermissionDecision`
- `from _decision import PermissionBehavior`
- `from _types import PermissionMode`

### 🏗️ 类 (Classes)
- `class PermissionEngine:`
- `    def __init__(...):`
- `    def add_rule(...):`
- `    def _convert_ask_to_deny(...):`
- `    def _is_safety_ask(...):`
- `    def _check_deny_rules(...):`
- `    def _check_ask_rules(...):`
- `    def _check_allow_rules(...):`
- `    def _rule_matches(...):`
- `    def _generate_suggestions(...):`

---

## 📄 agentscope/src/agentscope/permission/_rule.py
> **模块说明**: Permission rule model for tool usage.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from _types import PermissionBehavior`

### 🏗️ 类 (Classes)
- `class PermissionRule(BaseModel):`

---

## 📄 agentscope/src/agentscope/permission/_types.py
> **模块说明**: Permission system types and engine for tool usage control.

### 📦 依赖 (Imports)
- `from enum import Enum`

### 🏗️ 类 (Classes)
- `class PermissionMode(Enum):`
- `class PermissionBehavior(Enum):`

---

## 📄 agentscope/src/agentscope/skill/__init__.py
> **模块说明**: The skill related classes and functions.

### 📦 依赖 (Imports)
- `from _base import SkillLoaderBase`
- `from _base import Skill`
- `from _local_loader import LocalSkillLoader`

---

## 📄 agentscope/src/agentscope/skill/_base.py
> **模块说明**: The skill loader base class.

### 📦 依赖 (Imports)
- `from abc import abstractmethod`
- `from abc import ABC`
- `from dataclasses import dataclass`

### 🏗️ 类 (Classes)
- `class Skill:`
- `class SkillLoaderBase(ABC):`

---

## 📄 agentscope/src/agentscope/skill/_local_loader.py
> **模块说明**: The local skill loader class.

### 📦 依赖 (Imports)
- `import asyncio`
- `import os`
- `import aiofiles`
- `import aiofiles.ospath`
- `import frontmatter`
- `from _base import SkillLoaderBase`
- `from _logging import logger`
- `from skill import Skill`

### 🏗️ 类 (Classes)
- `class LocalSkillLoader(SkillLoaderBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/state/__init__.py
> **模块说明**: The agent state module in agentscope.

### 📦 依赖 (Imports)
- `from _state import AgentState`
- `from _state import TaskContext`
- `from _task import Task`

---

## 📄 agentscope/src/agentscope/state/_state.py
> **模块说明**: The agent state class.

### 📦 依赖 (Imports)
- `import uuid`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `import aiofiles.os`
- `from _task import Task`
- `from message import TextBlock`
- `from message import DataBlock`
- `from message import Msg`
- `from permission import PermissionContext`

### 🏗️ 类 (Classes)
- `class ReadCacheEntry(BaseModel):`
- `class ToolContext(BaseModel):`
- `class TaskContext(BaseModel):`
- `class AgentState(BaseModel):`

---

## 📄 agentscope/src/agentscope/state/_task.py
> **模块说明**: The task class.

### 📦 依赖 (Imports)
- `import uuid`
- `from datetime import datetime`
- `from typing import Any`
- `from typing import Literal`
- `from pydantic import BaseModel`
- `from pydantic import Field`

### 🏗️ 类 (Classes)
- `class Task(BaseModel):`

---

## 📄 agentscope/src/agentscope/tool/__init__.py
> **模块说明**: The tool module in agentscope.

### 📦 依赖 (Imports)
- `from _types import ToolChoice`
- `from _types import Function`
- `from _types import RegisteredTool`
- `from _response import ToolResponse`
- `from _response import ToolChunk`
- `from _toolkit import Toolkit`
- `from _base import ToolBase`
- `from _base import ParamsBase`
- `from _adapters import MCPTool`
- `from _adapters import FunctionTool`
- `from _builtin import ResetTools`
- `from _builtin import Bash`
- `from _builtin import Edit`
- `from _builtin import Glob`
- `from _builtin import Grep`
- `from _builtin import Read`
- `from _builtin import Write`
- `from _task import TaskUpdate`
- `from _task import TaskGet`
- `from _task import TaskList`
- `from _task import TaskCreate`
- `from _tool_group import ToolGroup`

---

## 📄 agentscope/src/agentscope/tool/_adapters.py
> **模块说明**: Adapters to convert functions and MCP tools to ToolProtocol.

### 📦 依赖 (Imports)
- `import inspect`
- `import json`
- `import re`
- `from contextlib import _AsyncGeneratorContextManager`
- `from datetime import timedelta`
- `from typing import Callable`
- `from typing import Any`
- `from typing import AsyncGenerator`
- `from typing import Generator`
- `from mcp import ClientSession`
- `import mcp`
- `from _types import Function`
- `from _base import ToolBase`
- `from permission import PermissionBehavior`
- `from permission import PermissionDecision`
- `from _response import ToolChunk`
- `from _utils import _extract_func_description`
- `from _utils import _extract_input_schema`
- `from _logging import logger`
- `from message import TextBlock`
- `from message import DataBlock`
- `from message import Base64Source`
- `from message import URLSource`
- `from message import ToolResultState`

### 🏗️ 类 (Classes)
- `class FunctionTool(ToolBase):`
- `    def __init__(...):`
- `    def _convert_func_result_to_chunk(...):`
- `class MCPTool(ToolBase):`
- `    def __init__(...):`
- `    def _convert_mcp_content_to_blocks(...):`

---

## 📄 agentscope/src/agentscope/tool/_base.py
> **模块说明**: The tool protocol in agentscope.

### 📦 依赖 (Imports)
- `import os`
- `from abc import abstractmethod`
- `from abc import ABC`
- `from pathlib import Path`
- `from typing import AsyncGenerator`
- `from typing import Any`
- `from typing import List`
- `from pydantic import BaseModel`
- `from _constants import DEFAULT_DANGEROUS_FILES`
- `from _constants import DEFAULT_DANGEROUS_DIRECTORIES`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionRule`
- `from permission import PermissionBehavior`
- `from _response import ToolChunk`
- `from _utils import _remove_title_field`

### 🏗️ 类 (Classes)
- `class ParamsBase(BaseModel):`
- `    def model_json_schema(...):`
- `class ToolBase(ABC):`
- `    def match_rule(...):`
- `    def generate_suggestions(...):`
- `    def _path_in_allowed_working_path(...):`
- `    def _is_dangerous_path(...):`

---

## 📄 agentscope/src/agentscope/tool/_builtin/__init__.py
> **模块说明**: The builtin tools in agentscope.

### 📦 依赖 (Imports)
- `from _meta import ResetTools`
- `from _skill import SkillViewer`
- `from _bash import Bash`
- `from _edit import Edit`
- `from _glob import Glob`
- `from _grep import Grep`
- `from _read import Read`
- `from _write import Write`

---

## 📄 agentscope/src/agentscope/tool/_builtin/_bash.py
> **模块说明**: The bash tool in agentscope.

### 📦 依赖 (Imports)
- `import os`
- `from typing import AsyncGenerator`
- `from typing import Any`
- `from typing import List`
- `import re`
- `import asyncio`
- `from _bash_parser import BashCommandParser`
- `from _base import ToolBase`
- `from _constants import DEFAULT_DANGEROUS_FILES`
- `from _constants import DEFAULT_DANGEROUS_DIRECTORIES`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from permission import PermissionMode`
- `from permission import PermissionRule`
- `from message import TextBlock`
- `from _response import ToolChunk`

### 🏗️ 类 (Classes)
- `class Bash(ToolBase):`
- `    def __init__(...):`
- `    def match_rule(...):`
- `    def generate_suggestions(...):`
- `    def _extract_dangerous_paths_from_bash(...):`
- `    def _check_dangerous_removal_path(...):`
- `    def _is_dangerous_removal_path(...):`

### ⚡ 函数 (Functions)
- `def _subprocess_creation_kwargs(...):`

---

## 📄 agentscope/src/agentscope/tool/_builtin/_bash_parser.py
> **模块说明**: Bash command parser using tree-sitter for precise syntax analysis.

### 📦 依赖 (Imports)
- `from typing import List`
- `from typing import Optional`
- `from typing import Set`
- `from typing import Tuple`
- `import re`
- `import shlex`
- `import tree_sitter_bash`
- `from tree_sitter import Language`
- `from tree_sitter import Parser`
- `from tree_sitter import Node`
- `from _constants import DANGEROUS_NODE_TYPES`
- `from _constants import DANGEROUS_COMMANDS`

### 🏗️ 类 (Classes)
- `class BashCommandParser:`
- `    def __init__(...):`
- `    def is_read_only_command(...):`
- `    def _is_single_command_read_only(...):`
- `    def extract_file_paths(...):`
- `    def _extract_paths_from_node(...):`
- `    def _extract_paths_fallback(...):`
- `    def extract_redirections(...):`
- `    def _extract_redirections_from_node(...):`
- `    def extract_command_prefixes(...):`
- `    def split_compound_command(...):`
- `    def _extract_command_prefix(...):`
- `    def _find_first_simple_command(...):`
- `    def check_dangerous_command(...):`
- `    def check_sed_constraints(...):`
- `    def check_injection_risk(...):`
- `    def _walk_for_dangerous_nodes(...):`

---

## 📄 agentscope/src/agentscope/tool/_builtin/_edit.py
> **模块说明**: The edit tool in agentscope.

### 📦 依赖 (Imports)
- `import fnmatch`
- `import os`
- `from typing import Any`
- `from typing import List`
- `import aiofiles`
- `from _base import ToolBase`
- `from _constants import DEFAULT_DANGEROUS_FILES`
- `from _constants import DEFAULT_DANGEROUS_DIRECTORIES`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from permission import PermissionMode`
- `from permission import PermissionRule`
- `from _response import ToolChunk`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from state import AgentState`

### 🏗️ 类 (Classes)
- `class Edit(ToolBase):`
- `    def __init__(...):`
- `    def match_rule(...):`
- `    def generate_suggestions(...):`

---

## 📄 agentscope/src/agentscope/tool/_builtin/_glob.py
> **模块说明**: The glob tool in agentscope.

### 📦 依赖 (Imports)
- `import fnmatch`
- `import os`
- `import re`
- `from typing import Any`
- `from typing import List`
- `from _base import ToolBase`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from permission import PermissionRule`
- `from _response import ToolChunk`
- `from message import TextBlock`

### 🏗️ 类 (Classes)
- `class Glob(ToolBase):`
- `    def __init__(...):`
- `    def match_rule(...):`
- `    def generate_suggestions(...):`
- `    def glob_part_to_regex(...):`
- `    def collect_all(...):`
- `    def match_parts(...):`
- `    def glob_match(...):`

---

## 📄 agentscope/src/agentscope/tool/_builtin/_grep.py
> **模块说明**: The grep tool in agentscope.

### 📦 依赖 (Imports)
- `import asyncio`
- `import fnmatch`
- `import os`
- `import shutil`
- `from typing import Any`
- `from typing import List`
- `from typing import Literal`
- `from _base import ToolBase`
- `from _logging import logger`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from permission import PermissionRule`
- `from _response import ToolChunk`
- `from message import TextBlock`
- `from message import ToolResultState`

### 🏗️ 类 (Classes)
- `class RipgrepTimeoutError(Exception):`
- `    def __init__(...):`
- `class Grep(ToolBase):`
- `    def __init__(...):`
- `    def match_rule(...):`
- `    def generate_suggestions(...):`
- `    def _apply_head_limit(...):`

---

## 📄 agentscope/src/agentscope/tool/_builtin/_meta.py
> **模块说明**: The meta tool class.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from pydantic import Field`
- `from pydantic import create_model`
- `from jinja2 import Template`
- `from _tool_group import ToolGroup`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from _response import ToolChunk`
- `from _base import ToolBase`
- `from exception import DeveloperOrientedException`
- `from message import TextBlock`
- `from state import AgentState`

### 🏗️ 类 (Classes)
- `class ResetTools(ToolBase):`
- `    def __init__(...):`
- `    def input_schema(...):`

---

## 📄 agentscope/src/agentscope/tool/_builtin/_read.py
> **模块说明**: The read tool in agentscope.

### 📦 依赖 (Imports)
- `import fnmatch`
- `import os`
- `from typing import Any`
- `from typing import List`
- `import aiofiles`
- `from _base import ToolBase`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from permission import PermissionRule`
- `from _response import ToolChunk`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from state import AgentState`

### 🏗️ 类 (Classes)
- `class Read(ToolBase):`
- `    def __init__(...):`
- `    def match_rule(...):`
- `    def generate_suggestions(...):`

---

## 📄 agentscope/src/agentscope/tool/_builtin/_skill.py
> **模块说明**: The builtin skill viewer tool.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from typing import Callable`
- `from typing import Awaitable`
- `from exception import DeveloperOrientedException`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from _response import ToolChunk`
- `from _base import ToolBase`
- `from skill import Skill`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from state import AgentState`

### 🏗️ 类 (Classes)
- `class SkillViewer(ToolBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/tool/_builtin/_write.py
> **模块说明**: The write tool in agentscope.

### 📦 依赖 (Imports)
- `import fnmatch`
- `import os`
- `from pathlib import Path`
- `from typing import Any`
- `from typing import List`
- `import aiofiles`
- `from _base import ToolBase`
- `from _constants import DEFAULT_DANGEROUS_FILES`
- `from _constants import DEFAULT_DANGEROUS_DIRECTORIES`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`
- `from permission import PermissionMode`
- `from permission import PermissionRule`
- `from _response import ToolChunk`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from state import AgentState`

### 🏗️ 类 (Classes)
- `class Write(ToolBase):`
- `    def __init__(...):`
- `    def match_rule(...):`
- `    def generate_suggestions(...):`

---

## 📄 agentscope/src/agentscope/tool/_constants.py
> **模块说明**: Constants for tool permission system.

---

## 📄 agentscope/src/agentscope/tool/_response.py
> **模块说明**: The tool response class.

### 📦 依赖 (Imports)
- `import uuid`
- `from typing import List`
- `from typing import Literal`
- `from typing import Self`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from message import DataBlock`
- `from message import TextBlock`
- `from message import Base64Source`
- `from message import ToolResultState`

### 🏗️ 类 (Classes)
- `class ToolChunk(BaseModel):`
- `class ToolResponse(BaseModel):`
- `    def append_chunk(...):`

---

## 📄 agentscope/src/agentscope/tool/_task/__init__.py
> **模块说明**: Task planning tools for agents.

### 📦 依赖 (Imports)
- `from _create_task import TaskCreate`
- `from _get_task import TaskGet`
- `from _list_task import TaskList`
- `from _update_task import TaskUpdate`

---

## 📄 agentscope/src/agentscope/tool/_task/_create_task.py
> **模块说明**: The creating task tool class.

### 📦 依赖 (Imports)
- `from typing import Any`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _task_tool_base import _TaskToolBase`
- `from _response import ToolChunk`
- `from state import AgentState`
- `from state import Task`
- `from exception import DeveloperOrientedException`
- `from message import TextBlock`
- `from message import ToolResultState`

### 🏗️ 类 (Classes)
- `class _TaskCreateParams(BaseModel):`
- `class TaskCreate(_TaskToolBase):`

---

## 📄 agentscope/src/agentscope/tool/_task/_get_task.py
> **模块说明**: The get task tool class.

### 📦 依赖 (Imports)
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _task_tool_base import _TaskToolBase`
- `from _response import ToolChunk`
- `from state import AgentState`
- `from exception import DeveloperOrientedException`
- `from message import TextBlock`
- `from message import ToolResultState`

### 🏗️ 类 (Classes)
- `class _TaskGetParams(BaseModel):`
- `class TaskGet(_TaskToolBase):`

---

## 📄 agentscope/src/agentscope/tool/_task/_list_task.py
> **模块说明**: The task list tool class.

### 📦 依赖 (Imports)
- `from _task_tool_base import _TaskToolBase`
- `from _response import ToolChunk`
- `from _base import ParamsBase`
- `from state import AgentState`
- `from exception import DeveloperOrientedException`
- `from message import TextBlock`

### 🏗️ 类 (Classes)
- `class _TaskListParams(ParamsBase):`
- `class TaskList(_TaskToolBase):`

---

## 📄 agentscope/src/agentscope/tool/_task/_task_tool_base.py
> **模块说明**: The task tool base class, providing unified interface and permission

### 📦 依赖 (Imports)
- `from typing import Any`
- `from _base import ToolBase`
- `from permission import PermissionContext`
- `from permission import PermissionDecision`
- `from permission import PermissionBehavior`

### 🏗️ 类 (Classes)
- `class _TaskToolBase(ToolBase):`

---

## 📄 agentscope/src/agentscope/tool/_task/_update_task.py
> **模块说明**: The task updated tool class.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from _task_tool_base import _TaskToolBase`
- `from _response import ToolChunk`
- `from state import AgentState`
- `from exception import DeveloperOrientedException`
- `from message import TextBlock`
- `from message import ToolResultState`

### 🏗️ 类 (Classes)
- `class _TaskUpdateParams(BaseModel):`
- `class TaskUpdate(_TaskToolBase):`
- `    def _update_block_relation(...):`

---

## 📄 agentscope/src/agentscope/tool/_tool_group.py
> **模块说明**: The tool group class.

### 📦 依赖 (Imports)
- `from typing import Literal`
- `from typing import Sequence`
- `from mcp import MCPClient`
- `from _base import ToolBase`
- `from skill import SkillLoaderBase`
- `from skill import Skill`
- `from skill import LocalSkillLoader`

### 🏗️ 类 (Classes)
- `class ToolGroup:`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/tool/_toolkit.py
> **模块说明**: The toolkit class for tool calls in AgentScope.

### 📦 依赖 (Imports)
- `import asyncio`
- `import inspect`
- `from collections import OrderedDict`
- `from typing import AsyncGenerator`
- `from typing import Type`
- `from typing import Generator`
- `from typing import Sequence`
- `import mcp`
- `from jinja2 import Template`
- `from pydantic import BaseModel`
- `from pydantic import Field`
- `from pydantic import create_model`
- `from _builtin import ResetTools`
- `from _builtin import SkillViewer`
- `from _base import ToolBase`
- `from _response import ToolResponse`
- `from _response import ToolChunk`
- `from skill import SkillLoaderBase`
- `from skill import Skill`
- `from _types import RegisteredTool`
- `from _utils._common import _json_loads_with_repair`
- `from exception import DeveloperOrientedException`
- `from exception import ToolNotFoundError`
- `from exception import ToolGroupInactiveError`
- `from mcp import MCPClient`
- `from message import ToolCallBlock`
- `from message import TextBlock`
- `from message import ToolResultState`
- `from _tool_group import ToolGroup`
- `from _logging import logger`
- `from state import AgentState`

### 🏗️ 类 (Classes)
- `class Toolkit:`
- `    def __init__(...):`
- `    def _get_meta_tool_schema(...):`
- `    def clear(...):`

---

## 📄 agentscope/src/agentscope/tool/_types.py
> **模块说明**: The types for the tool module in AgentScope.

### 📦 依赖 (Imports)
- `from copy import deepcopy`
- `from dataclasses import dataclass`
- `from dataclasses import field`
- `from typing import Literal`
- `from typing import Type`
- `from typing import Any`
- `from typing import TypeAlias`
- `from typing import Coroutine`
- `from typing import AsyncGenerator`
- `from typing import Generator`
- `from typing import Awaitable`
- `from typing import Callable`
- `from pydantic import BaseModel`
- `from _response import ToolChunk`
- `from _base import ToolBase`
- `from _utils import _remove_title_field`

### 🏗️ 类 (Classes)
- `class RegisteredTool:`
- `    def __post_init__(...):`
- `    def get_tool_schema(...):`
- `class ToolChoice(BaseModel):`

---

## 📄 agentscope/src/agentscope/tool/_utils.py
> **模块说明**: The tool module utils.

### 📦 依赖 (Imports)
- `import inspect`
- `from typing import Any`
- `from typing import Dict`
- `from typing import Callable`
- `from docstring_parser import parse`
- `from pydantic import Field`
- `from pydantic import create_model`
- `from pydantic import ConfigDict`

### ⚡ 函数 (Functions)
- `def _remove_title_field(...):`
- `def _extract_func_description(...):`
- `def _extract_input_schema(...):`

---

## 📄 agentscope/src/agentscope/types/__init__.py
> **模块说明**: The types in agentscope

### 📦 依赖 (Imports)
- `from _hook import AgentHookTypes`
- `from _hook import ReActAgentHookTypes`
- `from _object import Embedding`
- `from _json import JSONPrimitive`
- `from _json import JSONSerializableObject`

---

## 📄 agentscope/src/agentscope/types/_hook.py
> **模块说明**: The agent hooks types.

### 📦 依赖 (Imports)
- `from typing import Literal`

---

## 📄 agentscope/src/agentscope/types/_json.py
> **模块说明**: The JSON related types

### 📦 依赖 (Imports)
- `from typing import TypeAlias`

---

## 📄 agentscope/src/agentscope/types/_object.py
> **模块说明**: The object types in agentscope.

### 📦 依赖 (Imports)
- `from typing import List`

---

## 📄 agentscope/src/agentscope/workspace/__init__.py
> **模块说明**: The workspace module in agentscope.

### 📦 依赖 (Imports)
- `from _base import WorkspaceBase`
- `from _local_workspace import LocalWorkspace`
- `from _offload_protocol import Offloader`
- `from _docker import DockerWorkspace`
- `from _e2b import E2BWorkspace`

---

## 📄 agentscope/src/agentscope/workspace/_base.py
> **模块说明**: WorkspaceBase — abstract interface for agent workspaces.

### 📦 依赖 (Imports)
- `import uuid`
- `from abc import abstractmethod`
- `from typing import Self`
- `from mcp import MCPClient`
- `from message import Msg`
- `from message import ToolResultBlock`
- `from skill import Skill`
- `from tool import ToolBase`

### 🏗️ 类 (Classes)
- `class WorkspaceBase:`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/workspace/_docker/__init__.py
> **模块说明**: Docker-backed workspace.

### 📦 依赖 (Imports)
- `from _docker_workspace import DockerWorkspace`

---

## 📄 agentscope/src/agentscope/workspace/_docker/_docker_workspace.py
> **模块说明**: DockerWorkspace — sandboxed workspace backed by a Docker container.

### 📦 依赖 (Imports)
- `import asyncio`
- `import base64`
- `import hashlib`
- `import io`
- `import json`
- `import mimetypes`
- `import os`
- `import posixpath`
- `import shlex`
- `import shutil`
- `import sys`
- `import tarfile`
- `import uuid`
- `from copy import deepcopy`
- `from dataclasses import dataclass`
- `from typing import Any`
- `from pydantic import AnyUrl`
- `from _logging import logger`
- `from mcp import MCPClient`
- `from message import Base64Source`
- `from message import DataBlock`
- `from message import Msg`
- `from message import TextBlock`
- `from message import ToolResultBlock`
- `from message import URLSource`
- `from skill import Skill`
- `from tool import ToolBase`
- `from _base import WorkspaceBase`
- `from _gateway_client import GatewayClient`
- `from _gateway_client import GatewayMCPClient`
- `from _make_dockerfile import CONTAINER_DATA_DIR`
- `from _make_dockerfile import CONTAINER_SESSIONS_DIR`
- `from _make_dockerfile import CONTAINER_SKILLS_DIR`
- `from _make_dockerfile import CONTAINER_WORKDIR`
- `from _make_dockerfile import DEFAULT_BASE_IMAGE`
- `from _make_dockerfile import DEFAULT_GATEWAY_PORT`
- `from _make_dockerfile import GATEWAY_CONFIG`
- `from _make_dockerfile import GATEWAY_HOME`
- `from _make_dockerfile import GATEWAY_LOG`
- `from _make_dockerfile import GATEWAY_SCRIPT`
- `from _make_dockerfile import GATEWAY_VENV`
- `from _make_dockerfile import prepare_build_context`

### 🏗️ 类 (Classes)
- `class _ExecResult:`
- `    def ok(...):`
- `class DockerWorkspace(WorkspaceBase):`
- `    def __init__(...):`

---

## 📄 agentscope/src/agentscope/workspace/_docker/_make_dockerfile.py
> **模块说明**: Dockerfile generation + build-context preparation for DockerWorkspace.

### 📦 依赖 (Imports)
- `import hashlib`
- `import importlib.resources`
- `import shutil`
- `import tempfile`
- `from pathlib import Path`
- `from _utils import _GATEWAY_BASE_REQUIREMENTS`
- `from _utils import _agentscope_source_root`
- `from _utils import _agentscope_version`
- `from _utils import _is_released_install`
- `from _utils import _is_source_ignored`
- `from _utils import _read_gateway_script_bytes`

### ⚡ 函数 (Functions)
- `def _read_template(...):`
- `def _source_ignore(...):`
- `def _hash_directory(...):`
- `def render_dockerfile(...):`
- `def _render_requirements(...):`
- `def compute_image_tag(...):`
- `def prepare_build_context(...):`

---

## 📄 agentscope/src/agentscope/workspace/_e2b/__init__.py
> **模块说明**: E2B-backed workspace package.

### 📦 依赖 (Imports)
- `from _e2b_workspace import E2BWorkspace`

---

## 📄 agentscope/src/agentscope/workspace/_e2b/_bootstrap.py
> **模块说明**: Bootstrap helpers for :class:`E2BWorkspace` first-time provisioning.

### 📦 依赖 (Imports)
- `import io`
- `import tarfile`
- `from _logging import logger`
- `from _utils import _GATEWAY_BASE_REQUIREMENTS`
- `from _utils import _agentscope_source_root`
- `from _utils import _is_source_ignored`

### ⚡ 函数 (Functions)
- `def _tar_filter(...):`
- `def build_source_tarball(...):`
- `def bootstrap_commands(...):`
- `def render_install_agentscope_cmd_released(...):`
- `def render_install_agentscope_cmd_dev(...):`
- `def log_bootstrap_attempt(...):`

---

## 📄 agentscope/src/agentscope/workspace/_e2b/_e2b_workspace.py
> **模块说明**: E2BWorkspace — sandboxed workspace backed by an E2B cloud sandbox.

### 📦 依赖 (Imports)
- `import asyncio`
- `import base64`
- `import hashlib`
- `import json`
- `import mimetypes`
- `import os`
- `import posixpath`
- `import shlex`
- `import uuid`
- `from copy import deepcopy`
- `from dataclasses import dataclass`
- `from typing import Any`
- `from pydantic import AnyUrl`
- `from _logging import logger`
- `from mcp import MCPClient`
- `from message import Base64Source`
- `from message import DataBlock`
- `from message import Msg`
- `from message import TextBlock`
- `from message import ToolResultBlock`
- `from message import URLSource`
- `from skill import Skill`
- `from tool import ToolBase`
- `from _base import WorkspaceBase`
- `from _gateway_client import GatewayClient`
- `from _gateway_client import GatewayMCPClient`
- `from _bootstrap import DEFAULT_GATEWAY_PORT`
- `from _bootstrap import DEFAULT_TEMPLATE`
- `from _bootstrap import DEFAULT_TIMEOUT`
- `from _bootstrap import DEV_SRC_TAR`
- `from _bootstrap import GATEWAY_CONFIG`
- `from _bootstrap import GATEWAY_HOME`
- `from _bootstrap import GATEWAY_LOG`
- `from _bootstrap import GATEWAY_SCRIPT`
- `from _bootstrap import GATEWAY_VENV_PY`
- `from _bootstrap import METADATA_WORKSPACE_ID_KEY`
- `from _bootstrap import SANDBOX_DATA_DIR`
- `from _bootstrap import SANDBOX_MCP_FILE`
- `from _bootstrap import SANDBOX_SESSIONS_DIR`
- `from _bootstrap import SANDBOX_SKILLS_DIR`
- `from _bootstrap import SANDBOX_WORKDIR`
- `from _bootstrap import bootstrap_commands`
- `from _bootstrap import build_source_tarball`
- `from _bootstrap import log_bootstrap_attempt`
- `from _bootstrap import render_install_agentscope_cmd_dev`
- `from _bootstrap import render_install_agentscope_cmd_released`
- `from _utils import _agentscope_version`
- `from _utils import _is_released_install`
- `from _utils import _read_gateway_script_bytes`

### 🏗️ 类 (Classes)
- `class _ExecResult:`
- `    def ok(...):`
- `class E2BWorkspace(WorkspaceBase):`
- `    def __init__(...):`
- `    def sandbox_id(...):`
- `    def _api_opts(...):`
- `    def _sandbox_proxy_headers(...):`

---

## 📄 agentscope/src/agentscope/workspace/_gateway_client.py
> **模块说明**: Host-side client for the in-workspace MCP gateway.

### 📦 依赖 (Imports)
- `import contextlib`
- `from typing import Any`
- `from typing import AsyncIterator`
- `import httpx`
- `import mcp.types`
- `from pydantic import PrivateAttr`
- `from mcp import MCPClient`
- `from message import ToolResultState`
- `from permission import PermissionBehavior`
- `from permission import PermissionDecision`
- `from tool import ToolBase`
- `from tool import ToolChunk`

### 🏗️ 类 (Classes)
- `class GatewayMCPTool(ToolBase):`
- `    def __init__(...):`
- `class GatewayMCPClient(MCPClient):`
- `    def model_post_init(...):`
- `    def attach(...):`
- `    def _wrap_tool(...):`
- `class GatewayClient:`
- `    def __init__(...):`
- `    def _client(...):`
- `    def _headers(...):`
- `    def make_client(...):`

### ⚡ 函数 (Functions)
- `def _bearer_headers(...):`
- `def _safe_detail(...):`

---

## 📄 agentscope/src/agentscope/workspace/_local_workspace.py
> **模块说明**: The local workspace class.

### 📦 依赖 (Imports)
- `import asyncio`
- `import base64`
- `import hashlib`
- `import json`
- `import mimetypes`
- `import os`
- `import re`
- `import shutil`
- `from copy import deepcopy`
- `from pathlib import Path`
- `from typing import TypedDict`
- `import aiofiles`
- `import aiofiles.ospath`
- `import frontmatter`
- `from pydantic import AnyUrl`
- `from _base import WorkspaceBase`
- `from mcp import MCPClient`
- `from message import TextBlock`
- `from message import DataBlock`
- `from message import ToolResultBlock`
- `from message import Msg`
- `from message import URLSource`
- `from message import Base64Source`
- `from skill import Skill`
- `from tool import ToolBase`
- `from tool import Bash`
- `from tool import Edit`
- `from tool import Glob`
- `from tool import Grep`
- `from tool import Read`
- `from tool import Write`
- `from _logging import logger`

### 🏗️ 类 (Classes)
- `class _SkillEntry(TypedDict):`
- `class _SkillsFile(TypedDict):`
- `class LocalWorkspace(WorkspaceBase):`
- `    def __init__(...):`

### ⚡ 函数 (Functions)
- `def _sanitize_dir_name(...):`

---

## 📄 agentscope/src/agentscope/workspace/_mcp_gateway/__init__.py
> **模块说明**: In-workspace MCP gateway package.

---

## 📄 agentscope/src/agentscope/workspace/_mcp_gateway/__main__.py
> **模块说明**: ``python -m agentscope.workspace._mcp_gateway`` entry point.

### 📦 依赖 (Imports)
- `from _mcp_gateway_app import main`

---

## 📄 agentscope/src/agentscope/workspace/_mcp_gateway/_mcp_gateway_app.py
> **模块说明**: In-workspace MCP gateway — FastAPI router over agentscope MCPClients.

### 📦 依赖 (Imports)
- `import argparse`
- `import asyncio`
- `import json`
- `from typing import Any`
- `from fastapi import Depends`
- `from fastapi import FastAPI`
- `from fastapi import HTTPException`
- `from fastapi import Request`
- `from fastapi.responses import PlainTextResponse`
- `from agentscope.mcp import MCPClient`

### 🏗️ 类 (Classes)
- `class _State:`
- `    def __init__(...):`

### ⚡ 函数 (Functions)
- `def _make_auth_dep(...):`
- `def _build_app(...):`
- `def main(...):`

---

## 📄 agentscope/src/agentscope/workspace/_offload_protocol.py
> **模块说明**: The offload protocol.

### 📦 依赖 (Imports)
- `from typing import Protocol`
- `from message import Msg`
- `from message import ToolResultBlock`

### 🏗️ 类 (Classes)
- `class Offloader(Protocol):`

---

## 📄 agentscope/src/agentscope/workspace/_utils.py
> **模块说明**: Host-side helpers shared by Docker + E2B backends.

### 📦 依赖 (Imports)
- `import importlib.resources`
- `from pathlib import Path`

### ⚡ 函数 (Functions)
- `def _is_source_ignored(...):`
- `def _agentscope_module_path(...):`
- `def _is_released_install(...):`
- `def _agentscope_version(...):`
- `def _agentscope_source_root(...):`
- `def _read_gateway_script_bytes(...):`

---
