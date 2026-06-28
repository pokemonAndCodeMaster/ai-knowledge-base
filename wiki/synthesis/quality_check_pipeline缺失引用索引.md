---
title: "quality_check_pipeline 缺失引用索引"
domain: ["ai_dlc", "tooling", "knowledge_mgmt"]
type: "synthesis"
tags: ["quality_check_pipeline", "缺失引用", "占位索引", "防幻觉"]
created: 2026-06-28
updated: 2026-06-28
sources: 38
status: active
related_code: []
affects_path: []
trigger_keywords: ["quality_check_pipeline缺失引用", "待人类补充", "断链"]
---

# quality_check_pipeline 缺失引用索引

38 个 source 共引用 146 个不同卡名；本轮摄入后仍有 102 个卡名没有原文。以下占位卡只焊接关系并明确缺口，不承载推测性内容。

反向来源：[[notebooklm_quality_check_pipeline]]、[[E2E数据管线枢纽核心设计文档]]。

## 其他上游依赖

- [[AI-DLC标准流程]]
- [[AutosenseIDExtractor]]
- [[CheckerBase 检查器根基类]]
- [[ClipDefinitionRepository]]
- [[ClipInfo 与 ClipInfoCollection]]
- [[ClipService]]
- [[DBServer数据库服务封装]]
- [[DI_URL工具_DiUrlUtils]]
- [[DataCheck核心数据类与辅助枚举]]
- [[DataCheck核心枚举定义]]
- [[DataCheck连接工具_ConnectUtils]]
- [[DataCheck项目全貌]]
- [[DataDownloader 数据下载器]]
- [[DatasetFormatter 数据集格式化器]]
- [[ExchangeRecord 交换记录模型]]
- [[FileReader多格式IO工具]]
- [[GaussDB-DWS建表避坑指南]]
- [[Norm-OpenCV_Import_RROS_Path_Guard]]
- [[OBS公共读取工具]]
- [[PKL并发读写工具]]
- [[PNC坐标解析器]]
- [[ParquetConverter (parquet.py)]]
- [[PgServer数据库连接器]]
- [[Ray分布式质检入口]]
- [[TimingCollector 时延收集器]]
- [[WorkerGuardian Worker全生命周期守护器]]
- [[YAML配置加载器]]
- [[src_llm 归一合并重构记录]]
- [[src_obs_OBS存储模块]]
- [[t_channel_dedup_lock 表]]
- [[t_clip_definition 表]]
- [[t_e2e_version 表]]
- [[t_god_e2e_mdc_data 表]]
- [[t_text_label_task 表]]
- [[仿真数据构造]]
- [[前端与API启动调试指南]]
- [[前端与API环境配置指南]]
- [[前端常见问题与排错指南]]
- [[华为OBS Moxing接口行为分析]]
- [[可选参数向后兼容设计]]
- [[场景树分类体系]]
- [[场景质检项映射规则]]
- [[批量标签提取链路]]
- [[数据质量一站式门户架构设计]]
- [[统一配置管理器]]
- [[质检主入口 DataCheck]]
- [[质检项元数据Schema]]
- [[配置管理架构重构教训：依赖注入→依赖查找]]

## LLM Pipeline 依赖

- [[BaseProducer 通道生产基类]]
- [[DedupLockManager 去重锁管理器]]
- [[DedupWatchdog 看门狗]]
- [[Dedup去重锁完整设计]]
- [[LLM Tools 关键算法]]
- [[LLM Tools 开发规范与设计决策]]
- [[LLM Tools 示例脚本索引]]
- [[LLM Tools 配置映射]]
- [[LLMBaseError 异常体系]]
- [[LLMInference LLM推理编排器]]
- [[TaskCreator 任务创建器]]
- [[TaskExecutor 任务生产执行器]]
- [[TaskOrchestrator 任务级状态轮询器]]
- [[TaskQueryService 任务聚合查询]]
- [[TaskRepository 任务DB读写封装层]]
- [[TaskWorker+TaskSchedulerApp 调度入口]]
- [[VideoConfig 视频配置模型]]
- [[VideoGenerator 视频生成器]]
- [[VideoProduction 视频生产编排器]]
- [[src_llm_production_通道生产包]]
- [[t_llm_task 表]]
- [[t_llm_version_config 表]]
- [[任务级vs通道级status架构设计]]
- [[通道解耦重构物理现状基线报告]]

## 规范与避坑

- [[DDL变更同步规范]]
- [[GaussDB-DWS建表SQL规范]]
- [[JSON 序列化性能陷阱：NumPy 类型泄漏的双层数据净化]]
- [[PF-ConfigManager_get签名陷阱]]
- [[PF-pg_connector_DatabaseConfig访问陷阱]]
- [[PGConnector接口语义陷阱：execute_query禁止写操作]]
- [[Python Import 位置规范]]
- [[Python Import 路径规范_绝对导入Only]]
- [[Python_Import位置规范_TopLevel_Only]]
- [[全局单例 ConfigManager 使用规范]]
- [[知识库双链层级规范]]
- [[知识库同步刷新规范]]
- [[质检标签YAML Schema规范]]
- [[软删除 is_deleted 设计规范]]

## 上游枢纽

- [[HUB-Clip标签Schema总览]]
- [[HUB-DAG任务流层架构]]
- [[HUB-DataCheck业务工具子集]]
- [[HUB-DataCheck配置与常量层]]
- [[HUB-Frame标签Schema总览]]
- [[HUB-clipinfo片段信息域]]
- [[HUB-pkl_vis可视化模块]]
- [[HUB-人工标注模块架构]]
- [[HUB-规控PKL模块]]
- [[HUB-规控标签模块]]

## 人工质检依赖

- [[人工质检-Delta平台API索引]]
- [[人工质检-数据库连接层]]
- [[人工质检-数据表索引]]
- [[人工质检-标准文本系统]]
- [[人工质检-状态枚举与公共定义]]
- [[人工质检-环境配置]]
