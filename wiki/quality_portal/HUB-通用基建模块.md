---
title: "通用基建模块"
domain: ["ai_dlc", "tooling"]
type: "hub"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_common_infra"]
created: 2026-06-28
updated: 2026-06-28
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["通用基建模块", "quality_check_pipeline", "common_infra"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["e0d4aa20-b8ef-491b-984b-34130dd2cb68"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/12_Copied text 1782623090_e0d4aa20.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

## NotebookLM 原始元数据快照

```yaml
id: "HUB-CI"
title: "通用基建模块"
domain: ["common_infra"]
type: "hub"

related_code: []
affects_path: []
trigger_keywords: ["common_infra", "基建", "配置", "数据库", "OBS", "序列化", "存储"]
tags: []
summary: "通用基建业务域的总入口，横跨存储、配置、数据库、序列化等底层能力，是所有业务域的公共底座。"
```
# 通用基建模块

通用基建业务域的总入口，横跨存储、配置、数据库、序列化等底层能力，是所有业务域的公共底座。

## 1. 核心业务流程

- [[AI-DLC标准流程]] — Agent 协作三步递进式 SOP
- [[可选参数向后兼容设计]] — API 演进三阶段迁移模式
- [[批量标签提取链路]] — OBS JSON → autosenseid 提取 → 标签查询 → Parquet 转换

## 2. 数据表定义

- [[t_clip_definition 表]] — 片段定义基础表
- [[t_god_e2e_mdc_data 表]] — 数据重产映射表
- [[t_e2e_version 表]] — 端到端版本管理表

## 3. 底层工具箱

- [[HUB-clipinfo片段信息域]] — clipinfo 域总入口（ClipInfo/ClipService/BatchLabelQuery/ParquetConverter 等）
- [[src_obs_OBS存储模块]] — ObsManager/ObsClient 高层+底层 OBS 操作封装
- [[src_database_数据库连接器模块]] — PGConnector 数据库原子连接能力（Mongo/BaseConnector 已于 TAG 20260626_000000 删除）
- [[统一配置管理器]] — 中央配置加载与分发，ConfigManager 单例 + get_global_config 唯一入口
- [[ClipService]] — Clip 查询统一门面（Facade）
- [[AutosenseIDExtractor]] — autosenseid 与时间区间解析器
- [[ClipInfo 与 ClipInfoCollection]] — 片段信息结构化数据模型
- [[ClipDefinitionRepository]] — 已废弃，合并入 [[ClipService]]

## 4. DataCheck Utils工具箱

- [[OBS公共读取工具]] — Obs类/多区域认证/try_obs_file_exist
- [[DataCheck连接工具_ConnectUtils]] — Clip信息获取/标签路径查询/数据路径拼接
- [[DBServer数据库服务封装]] — PG+Hive统一数据库访问层
- [[DI_URL工具_DiUrlUtils]] — DriveInsight API数据查询与URL构建
- [[FileReader多格式IO工具]] — 本地+OBS双模式多格式文件读取器
- [[PKL并发读写工具]] — ThreadPoolExecutor并发PKL读写
- [[PNC坐标解析器]] — Frenet(s-l)↔笛卡尔(x-y)坐标双向转换
- [[ParquetConverter (parquet.py)]] — Parquet文件读取/NumPy序列化/Frame标签转换（已迁移至 src/clipinfo/label/parquet.py）

## 5. 护栏与红线

- [[JSON 序列化性能陷阱：NumPy 类型泄漏的双层数据净化]] | 护栏拦截: src/clipinfo/*, src/llm/*
- [[配置管理架构重构教训：依赖注入→依赖查找]] | 护栏拦截: src/obs/*, src/clipinfo/*, scripts/batch_label_download/*
- [[全局单例 ConfigManager 使用规范]] | 护栏拦截: src/config/*, src/obs/obs_manager.py, src/obs/obs_client.py
- [[Norm-OpenCV_Import_RROS_Path_Guard|OpenCV cv2 导入防护规范 ROS 环境路径冲突]] | 护栏拦截: **/*.py (所有含 import cv2 的模块)
- [[华为OBS Moxing接口行为分析]] | 护栏拦截: src/obs/*, src/data_check/utils/common_read.py
- [[GaussDB-DWS建表SQL规范]] | 护栏拦截: scripts/sql/*, src/llm/*
- [[GaussDB-DWS建表避坑指南]] | 护栏拦截: scripts/sql/*, src/llm/*
- [[Python_Import位置规范_TopLevel_Only|Python Import 位置规范 Top-Level Import Only]] | 护栏拦截: **/*.py

## 6. 前端与API层

- [[HUB-前端与API层架构]] — Vue3+FastAPI 单端口部署架构总览
- [[前端与API环境配置指南]] — Node.js/Python 环境要求、.env + application.yaml 配置规范
- [[前端与API启动调试指南]] — 启动命令、联调方式、Swagger UI、热重载排错
- [[FastAPI后端API层架构]] — app.py 工厂函数、依赖注入、路由注册、Schema 设计
- [[Vue3前端层架构]] — 目录结构、路由、MainLayout 侧边栏、axios 封装
- [[TaskView交互流程详解]] — 任务列表/创建/杀死/清理完整交互链路
