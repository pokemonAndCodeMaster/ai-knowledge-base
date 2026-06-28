---
title: "E2E数据管线枢纽核心设计文档"
domain: ["knowledge_mgmt", "ai_dlc", "tooling"]
type: "hub"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_knowledge_mgmt", "原业务域_common_infra"]
created: 2026-06-28
updated: 2026-06-28
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["E2E数据管线枢纽核心设计文档", "quality_check_pipeline", "knowledge_mgmt", "common_infra"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["dd6045cd-7552-4ca9-ad1f-e96e0144ce13"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/08_Copied text 1782622959_dd6045cd.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

## NotebookLM 原始元数据快照

```yaml
id: "DOC-CORE-001"
title: "E2E数据管线枢纽核心设计文档"
domain: ["knowledge_mgmt", "common_infra"]
type: "hub"

related_code: []
affects_path: []
trigger_keywords: ["核心设计", "数据管线", "枢纽", "项目总纲", "架构总览", "E2E", "数据闭环"]
tags: ["核心文档", "项目总纲", "架构设计"]
summary: "E2E数据管线枢纽的项目级核心设计文档，统领全项目架构。以自动驾驶端到端数据生产为主线，串联大模型数据生产、自动化质检、人工质检、规控标签四大业务域，形成数据采集→生产→质检→标注→回写的完整闭环。"
```
# E2E数据管线枢纽核心设计文档

> 本文档是 `e2e_data_pipeline_hub` 项目的**顶层核心设计总纲**，统领全项目架构与业务域关系。所有模块级详细设计见知识库各 Hub 卡片，本文档负责提供全局视图与跨域关系。

## 一、项目定位

**面向自动驾驶端到端数据生产的 AI 智能体协作系统** —— 知识管理和软件开发的中枢。

本项目以 E2E（End-to-End）自动驾驶数据为主线，构建从数据采集、LLM 训练数据生产、自动化质检、人工标注到 Ground Truth 回写的完整闭环，并通过知识库系统沉淀全流程的架构设计、开发规范与经验教训。

### 核心价值

1. **数据闭环**：采集 → 生产 → 质检 → 标注 → 回写 → 迭代，形成数据飞轮
2. **AI 协作**：PM-Architect / Coder-Executor / QA-Verifier / Knowledge-Manager 四角色 Agent 协作开发
3. **知识沉淀**：双向链接的知识图谱系统，让知识不再是孤立文件而是相互关联的网络

## 二、全局架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                        E2E 数据管线枢纽                              │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │
│  │  大模型数据  │  │  自动化质检  │  │  人工质检    │  │ 规控标签  │ │
│  │   生产      │  │   引擎      │  │  (Delta)    │  │  Schema  │ │
│  │  (llm_qa)   │  │  (auto_qa)  │  │ (manual_qa) │  │(planning)│ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘ │
│         │                │                │               │       │
│         └────────────────┼────────────────┘               │       │
│                          ▼                                │       │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    通用基建 (common_infra)                    │ │
│  │   OBS存储 │ PostgreSQL │ 配置管理 │ Clip信息 │ 数据转换       │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                          │                                          │
│                          ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              前端与API层 (FastAPI + Vue3)                      │ │
│  │   /api/tasks │ /api/versions │ /api/evaluations │ /api/datasets│ │
│  │   质检任务   │  版本配置     │  模型评测        │  数据集管理  │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │              知识库 (knowledge_base)                          │ │
│  │   Wiki卡片 │ GLOBAL_INDEX黄页 │ TAXONOMY分类法 │ 双向链接图谱  │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## 三、业务域划分

项目按 `TAXONOMY.yaml` 定义的业务域组织，共 7 个 Domain：

| Domain | 中文名 | 核心模块 | 入口卡片 |
|--------|--------|----------|----------|
| `llm_qa` | 大模型数据生产与质检 | `src/llm/` | [[HUB-大模型数据生产与质检模块]] |
| `auto_qa` | 自动化质检 | `src/data_check/` | [[HUB-质检引擎层架构]] |
| `manual_qa` | 人工质检 | `src/data_check/manual_label/` | [[人工质检-Hub]] |
| `planning_pkl` | 规控PKL | `src/pkl_vis/`, `src/data_check/planning_pkl_yaml/` | [[HUB-规控PKL模块]] |
| `planning_label` | 规控标签 | `data_schemas/label_schema/` | [[HUB-规控标签模块]] |
| `common_infra` | 通用基建 | `src/obs/`, `src/database/`, `src/config/`, `src/clipinfo/` | [[HUB-通用基建模块]] |
| `knowledge_mgmt` | 知识管理元知识域 | `knowledge_base/`, `.opencode/` | [[HUB-Agent协作体系总览]] |

## 四、`src/` 代码架构

项目代码库已从 `tool_registry/` 三层架构迁移至 `src/` 二级扁平架构。

```
src/
├── config/          # 统一配置管理（ConfigManager 单例 + get_global_config）
├── obs/             # 华为云 OBS 文件管理（ObsManager）
├── database/        # PostgreSQL 连接器（PGConnector）
├── clipinfo/        # Clip 信息、标签查询、数据转换
├── llm/             # LLM 数据生产 + 任务调度系统
│   ├── production/  # 通道解耦新架构（7通道 Producer）
│   └── ...          # 视频生产、LLM推理、任务调度
├── pkl_vis/         # PKL 可视化引擎（vispy offscreen 渲染）
├── data_check/      # 数据质检引擎
│   ├── clip_checker/    # 70+ Label检查器 + 30+ PKL检查器
│   ├── scene_atomic/    # 场景原子能力预计算
│   ├── dags/            # Airflow DAG 任务流编排
│   ├── manual_label/    # 人工质检全流程
│   └── ...              # 配置、常量、工具
├── api/             # FastAPI 后端服务
└── frontend/        # Vue3 前端界面（Element Plus）
```

> 详见 [[HUB-src顶层架构]]

## 五、数据闭环主线

```
① 数据采集          ② LLM数据生产         ③ 自动化质检          ④ 人工标注          ⑤ GT回写
   │                   │                    │                    │                  │
   ▼                   ▼                    ▼                    ▼                  ▼
 OBS原始数据    →   视频生成         →   质检引擎执行       →   Delta平台标注    →   GT入库
 Clip信息提取       LLM推理              场景原子预计算          格式校验             中间表更新
 标签查询           数据集格式化          帧清洗                 验收通过/打回        质检预警
                    任务调度              结果入库               状态刷新             周报生成
```

### 各阶段核心模块

| 阶段 | 核心模块 | 关键能力 |
|------|----------|----------|
| ① 数据采集 | `src/obs/`, `src/clipinfo/` | OBS 文件管理、Clip 信息提取、标签批量查询、Parquet 转换 |
| ② LLM数据生产 | `src/llm/` | 视频生产编排、LLM 推理、数据集格式化、任务调度、通道解耦 |
| ③ 自动化质检 | `src/data_check/` | 70+ Label检查器、30+ PKL检查器、场景原子预计算、DAG编排 |
| ④ 人工标注 | `src/data_check/manual_label/` | Delta平台对接、预标注+LLM分流、标注审核、验收打回 |
| ⑤ GT回写 | `src/data_check/manual_label/` | GT入库、中间表更新、质检预警、周报生成 |

## 六、前端与API层

采用 **FastAPI + Vue3 单端口部署** 架构：

```
浏览器 (http://localhost:8000)
├─ /api/*    → FastAPI 路由 (JSON API)
└─ /*        → StaticFiles (frontend/dist/)
```

### API 端点

| 路由前缀 | 端点数 | 核心功能 | 状态 |
|----------|--------|----------|------|
| `/api/tasks` | 10+ | 质检任务 CRUD + 文件上传 | ✅ 已实现 |
| `/api/versions` | 3+ | 版本配置创建与查询 | ✅ 已实现 |
| `/api/evaluations` | 2 | 模型评测创建与报告 | 🔧 三期骨架 |
| `/api/datasets` | 2 | 数据集列表与格式化 | 🔧 四期骨架 |
| `/api/health` | 1 | 健康检查 | ✅ 已实现 |

> 详见 [[HUB-前端与API层架构]]

## 七、知识库体系

项目基于**双向链接的知识图谱系统**组织所有信息：

### 知识分类法

**Type（知识类型）**：`hub` | `schema` | `norm` | `pitfall` | `module_doc` | `concept` | `code_module` | `source` | `synthesis`

### 知识管理工作流

| 工作流 | 触发方式 | 职责 |
|--------|----------|------|
| `[query]` | 顺藤摸瓜查询 | 黄页定位 → 深度遍历 → 闭环交付 |
| `[ingest]` | 知识摄入 | 读TAXONOMY → 写卡片 → 双链焊死 → 黄页注册 |
| `[health]` | 知识体检 | 扫描死链 → 扫描孤岛 → 扫描冗余 → 输出报告 |
| `[compile]` | 编译索引 | 刷新 GLOBAL_INDEX.md + Wiki 统计 + 工具注册表 |

### 核心索引文件

| 文件 | 职责 |
|------|------|
| `knowledge_base/GLOBAL_INDEX.md` | 全局黄页索引，按 Domain 分组列出所有卡片 |
| `knowledge_base/TAXONOMY.yaml` | 分类法约束，定义允许的 Domain 和 Type |
| `knowledge_base/.wiki_graph.json` | 双向链接图谱（自动生成） |

> 详见 [[HUB-Agent协作体系总览]]

## 八、AI Agent 协作体系

项目采用 **AI-DLC（AI-Driven Life Cycle）** 三步递进式开发流程：

```
用户需求
    │
    ▼
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ PM-Architect │     │ Coder-Executor   │     │ QA-Verifier      │
│ 需求梳理     │ →   │ 按契约编码       │ →   │ 测试验证         │
│ KM 摸底调查  │     │ 输出执行日志     │     │ 输出测试报告     │
│ 输出图纸     │     │                  │     │                  │
│ 01_PLAN.md   │     │ 02_EXECUTION_LOG │     │ 03_TEST_REPORT   │
└─────────────┘     └──────────────────┘     └──────────────────┘
                                                      │
                                          ┌───────────┴───────────┐
                                          ▼                       ▼
                                    🟢 ALL-PASS              🔴 FAIL
                                    闭环 + KM刷新            分诊返工
```

### 四条路由

| 路由 | 场景 | 流程 |
|------|------|------|
| Route A | 纯知识查询 | → KM `[query]` |
| Route B | 敏捷运维 | → QA 远端命令 |
| Route C | 知识摄入 | → KM `[ingest]` |
| Route D | 标准开发 | PM → Coder → QA → KM `[kb-sync]` |

> 详见 [[HUB-Agent协作体系总览]]

## 九、环境与技术栈

### 后端

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | ≥ 3.9 | 运行时 |
| FastAPI | ≥ 0.111 | Web 框架 |
| uvicorn | ≥ 0.30 | ASGI 服务器 |
| pydantic | 2.11.7 | 数据校验 |
| psycopg2-binary | 2.9.9 | PostgreSQL 驱动 |
| openai | 2.17.0 | LLM 客户端 |
| moxing-framework | 2.3.11 | 华为云 OBS |
| opencv-python-headless | 4.11.0.86 | 视频处理 |
| loguru | 0.7.3 | 日志 |
| vispy | — | PKL 可视化 GPU 渲染 |

### 前端

| 依赖 | 版本 | 用途 |
|------|------|------|
| Node.js | ≥ 18 | 运行时 |
| Vue | ^3.5 | UI 框架 |
| Vite | ^5.4 | 构建工具 |
| TypeScript | ^5.6 | 类型系统 |
| Element Plus | ^2.9 | 组件库 |
| Axios | ^1.7.0 | HTTP 客户端 |

### 配置

| 配置文件 | 职责 |
|----------|------|
| `config/.env` | 密钥（DB密码、LLM API Key、OBS AK/SK） |
| `config/application.yaml` | 6大配置区（database/storage/app/data_check/llm_tools/task_scheduler） |

> 详见 [[前端与API环境配置指南]]

## 十、数据库

主数据库为 **PostgreSQL**（华为 GaussDB-DWS），schema `data_common_4`。

### 核心数据表

| 表名 | 用途 | 所属域 |
|------|------|--------|
| `t_llm_task` | LLM 任务调度核心表（6通道 status） | llm_qa |
| `t_llm_version_config` | 版本配置表（通道配置/processor 动态 import） | llm_qa |
| `t_channel_dedup_lock` | 通道级去重锁 | llm_qa |
| `t_clip_definition` | 片段定义基础表 | common_infra |
| `t_e2e_version` | 端到端版本管理表 | common_infra |
| `t_text_label_task` | 文本/场景描述类标签任务表 | manual_qa |
| `t_pnc_label_task` | 规控标签任务表 | planning_label |
| `t_e2e_quality_check_result_t_with_partition` | 质检结果表 | auto_qa |
| `t_god_e2e_mdc_data` | 数据重产映射表 | common_infra |

> 数据库变更脚本位于 `migrations/`，表结构文档位于 `data_schemas/`。详见 [[DDL变更同步规范]]。

## 十一、核心 Hub 卡片导航

### 项目级

- [[HUB-Agent协作体系总览]] — AI Agent 协作体系总入口
- [[HUB-src顶层架构]] — `src/` 代码架构总览与旧路径映射

### 业务域级

- [[HUB-大模型数据生产与质检模块]] — llm_qa 域总入口
- [[HUB-质检引擎层架构]] — auto_qa 质检引擎总入口
- [[HUB-DAG任务流层架构]] — Airflow DAG 任务流编排
- [[人工质检-Hub]] — manual_qa 人工质检全流程
- [[HUB-人工标注模块架构]] — 人工标注模块架构
- [[HUB-规控PKL模块]] — planning_pkl 域总入口
- [[HUB-规控标签模块]] — planning_label 域总入口
- [[HUB-Clip标签Schema总览]] — Clip 级标签 Schema
- [[HUB-Frame标签Schema总览]] — Frame 级标签 Schema

### 基建级

- [[HUB-通用基建模块]] — 通用基建域总入口
- [[HUB-clipinfo片段信息域]] — clipinfo 域总入口
- [[HUB-DataCheck配置与常量层]] — 质检配置层
- [[HUB-DataCheck业务工具子集]] — 质检业务工具
- [[HUB-pkl_vis可视化模块]] — PKL 可视化引擎

### 前后端一体化

- [[HUB-前端与API层架构]] — FastAPI + Vue3 单端口部署
- [[HUB-质检前后端一体化]] — 质检前后端一体化学习与开发
- [[质检前后端一体化理想架构设计]] — 理想架构设计
- [[Router_API_View与Python业务编排指南]] — Router/API/View 分层编排
- [[质检页签端到端开发流程指南]] — 端到端开发流程
- [[数据质量一站式门户架构设计]] — 门户架构设计
- [[前端可视化与组件复用工程指南]] — 前端可视化与组件复用

## 十二、核心开发规范

| 规范 | 适用范围 | 要点 |
|------|----------|------|
| [[LLM Tools 开发规范与设计决策]] | `src/llm/*` | 禁止 os.getenv() 读凭证；禁止 llm_tools 外新建配置段 |
| [[全局单例 ConfigManager 使用规范]] | `src/config/*` | 初始化在 __init__；多进程 for_multiprocess=True |
| [[前端开发规范]] | `src/frontend/*` | 禁止 any；scoped CSS；API 走 api 层 |
| [[前端与API环境配置指南]] | 全栈 | Python≥3.10, Node≥18, DB 连接规范 |
| [[前端与API启动调试指南]] | 全栈 | 启动命令、联调方式、端口占用处理 |
| [[DDL变更同步规范]] | `migrations/*` | DDL 变更需同步表结构文档 |
| [[软删除 is_deleted 设计规范]] | 新建表 | is_deleted + Partial Index |
| [[GaussDB-DWS建表SQL规范]] | `scripts/sql/*` | DISTRIBUTE BY HASH 必选 |
| [[Python Import 路径规范_绝对导入Only]] | `**/*.py` | 强制绝对导入 |
| [[Python Import 位置规范]] | `**/*.py` | import 在文件顶层 |
| [[知识库双链层级规范]] | `knowledge_base/wiki/**` | synthesis/concept 必须回链归属 Hub |
| [[知识库同步刷新规范]] | Route D 闭环 | QA-PASS 后、commit 前强制刷新知识库 |

## 十三、核心避坑指南

| 避坑卡 | 适用范围 | 教训 |
|--------|----------|------|
| [[华为OBS Moxing接口行为分析]] | `src/obs/*` | Moxing 接口行为特性与陷阱 |
| [[PGConnector接口语义陷阱：execute_query禁止写操作]] | `src/database/*` | execute_query 仅限 SELECT |
| [[PF-ConfigManager_get签名陷阱]] | `src/config/*` | get() 签名陷阱 |
| [[PF-pg_connector_DatabaseConfig访问陷阱]] | `src/database/*` | DatabaseConfig 访问方式 |
| [[JSON 序列化性能陷阱：NumPy 类型泄漏的双层数据净化]] | `src/clipinfo/*` | NumPy 类型泄漏防护 |
| [[配置管理架构重构教训：依赖注入→依赖查找]] | `src/obs/*` | 依赖注入到依赖查找的架构演进 |
| [[GaussDB-DWS建表避坑指南]] | `scripts/sql/*` | GaussDB-DWS 建表注意事项 |
| [[前端常见问题与排错指南]] | `src/frontend/*` | 前端开发常见问题 |

## 十四、演进路线

### 已完成

- ✅ `tool_registry/` → `src/` 扁平架构迁移
- ✅ ConfigManager 统一配置管理
- ✅ LLM 任务调度系统（6通道 + 去重锁 + 守护进程）
- ✅ 通道解耦新架构（production/ 7通道 Producer）
- ✅ 自动化质检引擎（70+ Label检查器 + 30+ PKL检查器）
- ✅ 人工质检全流程（Delta平台对接 15 步闭环）
- ✅ FastAPI + Vue3 前后端一体化
- ✅ AI Agent 协作体系（PM → Coder → QA → KM）
- ✅ 知识库双向链接图谱系统

### 进行中

- 🔧 质检前后端一体化开发规范样板（LLM 域先行）
- 🔧 模型评测模块（三期）
- 🔧 数据集管理模块（四期）

### 规划中

- 📋 Pinia 状态管理引入
- 📋 OpenAPI → TypeScript 类型自动生成
- 📋 Alembic 数据库迁移工具
- 📋 Playwright E2E 测试
- 📋 WebSocket 实时推送
- 📋 ECharts 数据可视化
- 📋 表单引擎
- 📋 国际化 i18n
- 📋 权限细化

## 关联卡片

- [[HUB-Agent协作体系总览]] — Agent 协作体系总入口
- [[HUB-src顶层架构]] — 代码架构总览
- [[HUB-通用基建模块]] — 通用基建总入口
- [[HUB-大模型数据生产与质检模块]] — LLM 域总入口
- [[HUB-质检引擎层架构]] — 质检引擎总入口
- [[人工质检-Hub]] — 人工质检总入口
- [[HUB-前端与API层架构]] — 前后端架构总入口
- [[HUB-质检前后端一体化]] — 前后端一体化学习与开发

> ⚠️ 本文档是项目级核心总纲，由 Knowledge-Manager 维护。如需修改架构设计，请先通过 PM-Architect 发起架构评审，再通过 Route D 流程更新。
