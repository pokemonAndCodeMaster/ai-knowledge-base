---
title: 质检一站式平台项目环境与开发规范总览
domain: ["ai_dlc", "agent_engineering", "tooling"]
type: "hub"
tags: [质检平台, e2e_data_pipeline_hub, 自动驾驶, 一站式平台, 开发规范, AI_DLC]
created: 2026-06-21
updated: 2026-06-21
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: [质检项目, e2e_data_pipeline_hub, 一站式平台, 环境配置, 开发流程, AI-DLC]
---

# 质检一站式平台项目环境与开发规范总览

本卡是质检项目组一站式平台的导航枢纽。项目定位是面向自动驾驶端到端数据生产的 AI 智能体协作系统，兼具知识管理、任务调度、数据质检、LLM 数据生产、API 服务和前端运营界面。

## 当前系统边界

- `src/obs/`：华为云 OBS 文件管理，核心入口 `ObsManager`。
- `src/database/`：PostgreSQL 与 MongoDB 连接器，核心入口 `DatabaseManager` / `MongoConnector`。
- `src/config/`：统一配置管理，核心入口 `ConfigManager` / `get_global_config()`。
- `src/clipinfo/`：Clip 信息、标签查询、Parquet 转换、Frenet 坐标转换。
- `src/llm/`：LLM 数据生产、视频生成、推理调用、任务调度系统。
- `src/pkl_vis/`：基于 vispy 的 PKL offscreen 可视化视频生成。
- `src/data_check/`：Celery-Ray 分布式数据质检，包含 PKL 检查器与标签检查器。
- `src/api/`：FastAPI 后端服务，详见 [[FastAPI后端API层架构]]。
- `src/frontend/`：Vue3 前端界面，详见 [[Vue3前端层架构]]。

## 配置与环境

`config/application.yaml` 是运行时配置中心，至少覆盖：

- `database`：PostgreSQL/MongoDB 连接池与查询配置。
- `storage`：华为云 OBS 端点、Bucket、传输配置。
- `app`：日志、缓存、临时文件等应用级配置。
- `data_check`：质检 Region 路由、环境变量注入、数据库别名映射。
- `llm_tools`：视频生产、LLM 推理、默认 Prompt 配置。
- `task_scheduler`：任务调度数据库、轮询间隔、Worker 并发数、OBS 上传通道。

环境变量至少包含数据库密码、LLM API Key、OBS 访问密钥和特定 Bucket 密钥。涉及华为特有包时，按 `requirements.txt` 注释中的专用源安装。

## 已实现产品面

- `/task`：质检任务。支持任务创建、监控、进度查看、回收站和清理。
- `/version`：版本配置。支持模型、视频、Prompt 等版本参数管理。
- `/eval`：模型评测，当前是三期骨架。
- `/dataset`：数据集管理，当前是四期骨架。

后端 API 状态：

- `/api/tasks`：质检任务 CRUD、文件上传、任务组概览、进度和吞吐，已实现。
- `/api/versions`：版本配置创建、查询、详情，已实现。
- `/api/evaluations`：模型评测创建与报告，骨架。
- `/api/datasets`：数据集列表与格式化，骨架。
- `/api/health`：健康检查，已实现。

## 标准开发闭环

项目采用 AI-DLC：规划 → 实施 → 验证 → 知识沉淀。

- 规划：需求澄清、知识检索、模块现状摸底，必要时产出 `.artifacts/01_PLAN_<TAG>.md`。
- 实施：按契约修改代码，必要时产出 `.artifacts/02_EXECUTION_LOG_<TAG>.md`。
- 验证：优先端到端验证任务创建、调度、查询、页面交互等真实路径，必要时产出 `.artifacts/03_TEST_REPORT_<TAG>.md`。
- 知识沉淀：新增规范、坑点、模块地图或失效信息必须回写 wiki、`index.md`、`log.md` 并重编译图谱。

## 关联卡片

- [[LLM任务调度Pipeline全景]]
- [[HUB-前端与API层架构]]
- [[FastAPI后端API层架构]]
- [[Vue3前端层架构]]
- [[TaskView交互流程详解]]
- [[VersionView版本配置页面交互详解]]
- [[质检一站式平台长期架构]]
