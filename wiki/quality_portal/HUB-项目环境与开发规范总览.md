---
title: "e2e_data_pipeline_hub 项目环境与开发规范总览"
domain: ["ai_dlc", "tooling"]
type: "hub"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入"]
created: 2026-06-28
updated: 2026-06-28
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["e2e_data_pipeline_hub 项目环境与开发规范总览", "quality_check_pipeline"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["560ccc19-d420-4de5-853e-c990841b155d"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/07_Copied text 1781950770_560ccc19.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。
# 🚗 e2e_data_pipeline_hub

> **项目定位**：面向自动驾驶端到端数据生产的 AI 智能体协作系统 —— 知识管理和软件开发的中枢。

---

## 一、环境配置

### 1.1 前置条件

- Python ≥ 3.9
- Node.js ≥ 18（前端开发）
- Git

### 1.2 克隆项目

```bash
git clone <repository_url>
cd e2e_data_pipeline_hub
```

### 1.3 安装 Python 依赖

```bash
pip install -r requirements.txt
```

> ⚠️ 华为特有包（moxing-framework、hw-ads-di-* 等）需特殊 pip 源，参见 `requirements.txt` 中的注释说明，取消对应行注释并使用指定 `--index-url` 安装。

### 1.4 配置环境变量

```bash
cp config/.env.example config/.env
```

编辑 `config/.env`，填写 4 类密钥：

| 类别 | 变量示例 | 用途 |
|------|----------|------|
| 数据库密码 | `DB_PERCEPTION_PASSWORD` | PostgreSQL 连接认证 |
| LLM API 密钥 | `LLM_API_KEY` | 大模型推理服务调用 |
| OBS 访问密钥 | `OBS_YW_AK` / `OBS_YW_SK` | 华为云 OBS 对象存储 |
| Bucket 特定密钥 | `OBS_BUCKET_ADS_CLOUD_GY_Y_AK` | 特定 Bucket 访问 |

### 1.5 应用配置说明

`config/application.yaml` 包含 6 大配置区：

| 配置区 | 一句话简介 |
|--------|-----------|
| database | PostgreSQL/MongoDB 连接池与查询配置 |
| storage | 华为云 OBS 端点、Bucket、传输配置 |
| app | 日志、缓存、临时文件等应用级配置 |
| data_check | 质检 Region 路由、环境变量注入、数据库别名映射 |
| llm_tools | 视频生产、LLM 推理、默认 Prompt 配置 |
| task_scheduler | 任务调度数据库、轮询间隔、Worker 并发数、OBS 上传通道 |

### 1.6 启动后端服务

```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

### 1.7 启动前端服务

```bash
cd src/frontend
npm install
npm run dev
```

前端开发服务器默认 `http://localhost:5173`，`/api` 请求自动代理到 `http://localhost:8000`（参见 `vite.config.ts`）。

### 1.8 pkl_vis GPU 环境配置

pkl_vis 模块使用 vispy 进行 offscreen 渲染，支持两种 GPU 方案：

- **EGL（推荐）**：有 NVIDIA GPU 时自动使用，无需 X11
- **OSMesa**：无 GPU 环境的软件渲染回退

详见 → [`src/pkl_vis/INSTALL.md`](src/pkl_vis/INSTALL.md)

---

## 二、项目目录与模块介绍

### 2.1 顶层目录树

```
e2e_data_pipeline_hub/
├── 📁 config/          ⚙️ 统一配置（.env、application.yaml）
├── 📁 src/             🏗️ 核心代码库（9 个子模块）
├── 📁 scripts/         🔧 独立脚本工具
├── 📁 knowledge_base/  📚 知识库（Wiki 卡片 + 索引 + 脚本）
├── 📁 migrations/      🗃️ 数据库变更 SQL
├── 📁 data_schemas/    📋 数据表结构文档
├── 📁 tests/           🧪 测试用例
├── 📄 requirements.txt 📦 Python 依赖清单
└── 📄 README.md        📖 本文档
```

### 2.2 `src/` 核心模块一览

| 模块 | emoji | 功能 | 核心入口 |
|------|-------|------|----------|
| obs | ☁️ | 华为云 OBS 文件管理 | `ObsManager` |
| database | 🗄️ | PostgreSQL/MongoDB 连接器 | `DatabaseManager` / `MongoConnector` |
| config | ⚙️ | 统一配置管理（全局单例） | `ConfigManager` / `get_global_config()` |
| clipinfo | 📎 | Clip 信息、标签查询、数据转换 | `ClipService` / `BatchLabelQuery` |
| llm | 🤖 | LLM 数据生产 + 任务调度系统 | `VideoProduction` / `TaskSchedulerApp` |
| pkl_vis | 🎥 | PKL 可视化引擎 | `generate_video()` |
| data_check | 🔍 | 数据质检引擎 | `DataCheckApp` |
| api | 🌐 | FastAPI 后端服务 | `create_app()` |
| frontend | 💻 | Vue3 前端界面 | — |

---

## 三、模块使用方式

### 3.1 OBS 存储操作 (`src/obs/`)

华为云 OBS 文件上传、下载、列举、删除。

核心入口：`ObsManager`

📁 示例：`src/obs/example/obs_example.py` — OBS 文件上传下载基本操作

### 3.2 数据库连接器 (`src/database/`)

PostgreSQL 与 MongoDB 连接管理、连接池配置。

核心入口：`DatabaseManager` / `MongoConnector`

📁 示例：`src/database/example/database_example.py` — 数据库连接与查询操作

### 3.3 统一配置管理 (`src/config/`)

全局单例 ConfigManager，支持 .env/YAML 配置加载、多进程 pickle 序列化。

核心入口：`ConfigManager` / `get_global_config()`

📁 示例：`src/config/example/config_example.py` — 配置加载与使用方式

### 3.4 Clip 信息与数据转换 (`src/clipinfo/`)

ClipInfo 数据模型、标签查询、Parquet 转换、Frenet 坐标转换。

核心入口：`ClipService` / `BatchLabelQuery` / `ParquetConverter`

📁 示例：`src/clipinfo/example/clipinfo_example.py` — Clip 信息查询与标签处理

### 3.5 LLM 数据生产与任务调度 (`src/llm/`)

视频生产编排、LLM 推理、数据集格式化、任务调度系统。

核心入口：`VideoProduction` / `LLMInference` / `TaskSchedulerApp`

📁 示例：`src/llm/example/llm_video_task_example.py` — 视频生产任务完整流程

📁 示例：`src/llm/example/llm_inference_example.py` — LLM 推理调用示例

### 3.6 PKL 可视化引擎 (`src/pkl_vis/`)

基于 vispy 的 offscreen 渲染，生成自动驾驶场景可视化视频。

核心入口：`generate_video()`

📁 示例：`src/pkl_vis/example/pkl_vis_example.py` — PKL 数据可视化视频生成

### 3.7 数据质检引擎 (`src/data_check/`)

Celery-Ray 分布式质检，含 PKL 检查器与标签检查器。

核心入口：`DataCheckApp`

> 📁 暂无独立 example 文件，参见 `src/data_check/` 下各子模块文档。

### 3.8 独立脚本工具 (`scripts/`)

| 脚本 | 说明 |
|------|------|
| `scripts/batch_label_download/` | 批量标签下载：OBS 递归枚举 → JSON 下载 → 标签查询 → Parquet 转换 → 时间过滤输出 |
| `scripts/xlsx_to_pipeline_json.py` | XLSX 压线标注表格转 Pipeline JSON 格式 |

### 3.9 API 与前端

**后端 API 端点清单**

| 路由前缀 | 端点数 | 核心功能 | 实现状态 |
|----------|--------|----------|----------|
| `/api/tasks` | 10+ | 质检任务 CRUD + 文件上传 | ✅ 已实现 |
| `/api/versions` | 3+ | 版本配置创建与查询 | ✅ 已实现 |
| `/api/evaluations` | 2 | 模型评测创建与报告 | 🔧 三期骨架 |
| `/api/datasets` | 2 | 数据集列表与格式化 | 🔧 四期骨架 |
| `/api/health` | 1 | 健康检查 | ✅ 已实现 |

**前端页签路由**

| 路径 | 页签名 | 功能 |
|------|--------|------|
| `/task` | 质检任务 | 任务创建、监控、进度查看 |
| `/version` | 版本配置 | 版本参数管理 |
| `/eval` | 模型评测 | 评测任务与报告（开发中） |
| `/dataset` | 数据集管理 | 数据集浏览与格式化（开发中） |

---

## 四、标准开发流程

### 4.1 AI-DLC 开发流程

系统采用 AI-DLC（AI-Driven Life Cycle）三步递进式开发流程：**规划 → 实施 → 验证**，每步都有明确的契约文件和交付物。

1. **PM-Architect**：需求梳理 → KM 摸底调查 → 头脑风暴 → 输出 `01_PLAN.md`
2. **Coder-Executor**：按契约编码 → 输出 `02_EXECUTION_LOG.md`
3. **QA-Verifier**：远端测试验证 → 输出 `03_TEST_REPORT.md`
4. **智能分诊**：🟢 ALL-PASS 闭环 / 🟡 代码级 Bug 回退 Coder / 🔴 架构级缺陷回退 PM

详见 → [[HUB-Agent协作体系总览]]

### 4.2 契约文件体系

所有契约文件存放在 `.artifacts/` 目录，是 Agent 间协作的唯一正式交接通道：

| 契约文件 | 产出者 | 核心内容 |
|----------|--------|----------|
| `01_PLAN.md` | PM-Architect | 四级契约图纸：架构级 → 模块级 → 文件级 → 函数级 |
| `02_EXECUTION_LOG.md` | Coder-Executor | 三清单交接日志：变更清单 → 待验证清单 → 待清理清单 |
| `03_TEST_REPORT.md` | QA-Verifier | 测试报告：结论 + 详细验证结果 + 报错堆栈 |

### 4.3 知识管理

项目基于双向链接的知识图谱系统组织所有信息，通过 Domain/Type 双维度分类法，让知识不再是孤立的文件而是相互关联的网络。

- **[query]** 顺藤摸瓜查询 — **[ingest]** 知识摄入与双链焊死 — **[health]** 知识体检侦察
- 黄页索引：`knowledge_base/GLOBAL_INDEX.md`
- 分类约束：`knowledge_base/TAXONOMY.yaml`

详见 → [[HUB-Agent协作体系总览]]

### 4.4 数据库变更

- 变更脚本：`migrations/` 目录，按日期命名（如 `20260617_add_holder_id_to_dedup_lock.sql`）
- 表结构文档：`data_schemas/DB_INDEX.md` — 数据库表索引与说明
