---
title: "人工质检-Hub"
domain: ["ai_dlc", "agent_evaluation", "tooling"]
type: "hub"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_manual_qa", "原业务域_common_infra"]
created: 2026-06-28
updated: 2026-07-03
sources: 2
status: active
related_code: []
affects_path: []
trigger_keywords: ["人工质检-Hub", "quality_check_pipeline", "manual_qa", "common_infra"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["3b56b822-fb32-4f9a-892a-b5dddc380440", "f6c77380-21b5-49a5-940f-d75e02723cfc"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/09_Copied text 1782622984_3b56b822.md", "raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/17_Copied text 1782623215_f6c77380.md"]
---

> 🔄 当前仓库人工质检平台设计入口：[[质检一站式平台人工质检模块整体架构]]。产品前端导航：[[人工质检-交付任务与行动项机制]]、[[质检平台-人工质检交付中心前端设计]]、[[质检平台-人工质检验收中心前端设计]]。本卡继续保留上游十五步流程事实。
> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

> NotebookLM 中存在 2 份字节级重复 source；本卡合并编纂，原始文件均独立保留。

## NotebookLM 原始元数据快照

```yaml
id: "MH-HUB-001"
title: "人工质检-Hub"
domain: ["manual_qa", "common_infra"]
type: "hub"

related_code: ["src/data_check/manual_label/"]

affects_path: ["src/data_check/manual_label/*", "src/data_check/manual_label/human_inspection/*", "src/data_check/manual_label/vpd_inspection/*", "src/data_check/manual_label/batch_acceptance/*", "src/data_check/manual_label/quality_warning/*", "src/data_check/manual_label/middleware_table_process/*"]
trigger_keywords: ["人工质检", "manual_label", "Delta", "标注", "验收", "打回", "GT回写", "预警", "周报"]
tags: ["人工质检", "Delta平台", "标注流程", "验收", "GT", "预警"]
summary: "人工质检(Human Inspection)数据闭环总枢纽，覆盖从视频数据源接入、标注任务创建、预标注+LLM分流、Delta平台任务分配、标注审核、格式校验、验收通过/打回、GT回写、中间表更新到质检预警与周报的全流程，同时索引核心数据表、Delta平台API、公共基础设施和已知架构问题。"
code_hash: {}
```
# 人工质检-Hub

> 人工质检（Manual Label / Human Inspection）是数据闭环中对自动化质检结果的补充验证流程，通过 Delta 标注平台分配标注员、审核员、验收员完成多轮人工判定，最终产出 Ground Truth 入库。

## 📌 流程全景

```
①视频数据同步 → ②文本任务创建 → ③预标注+LLM/FDE决策 → ④Delta平台创建任务
→ ⑤任务分配 → ⑥标注+审核 → ⑦格式校验 → ⑧验收分配
→ ⑨批量通过/打回 → ⑩状态刷新+GT回写 → ⑪中间表更新 → ⑫质检预警 → ⑬周报
→ ⑭重复数据清理 → ⑮OBS审计日志
```

## 🏗️ 流程阶段索引

| 阶段 | 包含步骤 | 详细卡片 |
|------|---------|---------|
| 数据源接入与任务创建 | ①②③④⑤ | [[人工质检-数据源与任务创建]] |
| 标注执行与格式校验 | ⑥⑦ | [[人工质检-标注执行与格式校验]] |
| 验收与通过/打回 | ⑧⑨ | [[人工质检-验收与通过打回]] |
| GT回写与中间表 | ⑩⑪⑭⑮ | [[人工质检-GT回写与中间表]] |
| 质检预警与报表 | ⑫⑬ | [[人工质检-预警与报表]] |

### 步骤级详细卡片

- [[人工质检-①视频数据同步]] — 从cog_fusion拉取视频数据，增量同步到视频中间表
- [[人工质检-②文本任务创建]] — 将视频数据组装为文本标注任务(pending状态)
- [[人工质检-③预标注与LLM决策]] — 预标注填充+LLM/FDE分流决策(打桩vs走人工)
- [[人工质检-④Delta平台创建任务]] — 通过Delta平台API(addMainTask)创建标注任务，进入waitingAssign
- [[人工质检-⑤任务分配]] — 批量分配screener/reviewer/acceptor，Dry run→Wet run两步确认
- [[人工质检-⑥标注与审核]] — 标注员审核员在Delta平台内部操作，筛选流状态64→68
- [[人工质检-⑦格式校验]] — Airflow定时DAG自动检查标注格式，不合格taskRollback打回
- [[人工质检-⑧验收分配]] — Good/Bad分层抽样分配验收人，e2e双池/VPD单池轮询
- [[人工质检-⑨批量通过打回]] — 基于通过率看板自动判定批量通过/打回，do_pass三步/do_revoke两步
- [[人工质检-⑩状态刷新与GT回写]] — 同步Delta状态+TextParser解析GT+写入新旧质量表+Stub打桩
- [[人工质检-⑪中间表更新]] — 拉取标注记录构建状态时间线，写入中间表供看板消费
- [[人工质检-⑫质检预警]] — 基于规则+统计的质检预警，企微通知+预警表记录
- [[人工质检-⑬周报]] — 生成周报Excel和折线图
- [[人工质检-⑭重复数据清理]] — t_dq_e2e_label_gt重复记录IOU判定清理
- [[人工质检-⑮OBS审计日志]] — 入库操作审计日志(JSONL+OBS)

## 🗄️ 核心数据表索引

→ [[人工质检-数据表索引]]

## 🔌 Delta平台API索引

→ [[人工质检-Delta平台API索引]]

## 🏛️ 公共基础设施索引

| 基础设施 | 详细卡片 |
|---------|---------|
| 数据库连接层 | [[人工质检-数据库连接层]] |
| 标准文本系统 | [[人工质检-标准文本系统]] |
| 环境配置 | [[人工质检-环境配置]] |
| 状态枚举与公共定义 | [[人工质检-状态枚举与公共定义]] |

## 📂 代码目录结构

```
manual_label/
├── human_inspection/       # 驾驶行为质检(e2e)核心流程
├── vpd_inspection/         # VPD质检核心流程
├── tag_inspection/         # Tag标注任务
├── label_task_manage/      # 任务分配管理(旧版)
├── batch_acceptance/       # 批量验收
├── quality_warning/        # 质检预警
├── middleware_table_process/ # 中间表处理
├── stand_text/             # 标准文本系统
├── models/                 # 数据模型层
├── utils/                  # 工具函数
├── label_common_def.py     # 公共定义(TaskStatus/WhoLabel/ClipInfo)
├── task_manager_base.py    # 任务管理基类
├── create_base.py          # 任务创建基类
├── delete_duplicate_records.py  # 重复数据清理
├── migrate_god_to_pnc.py   # 旧表→新表全量迁移
└── ...
```

## 🏷️ 项目类型

| 类型 | project_name | 默认reviewer | ide_task_id |
|------|-------------|-------------|------------|
| e2e(驾驶行为质检) | `驾驶行为质检` | E2E_DEFAULT_REVIEWER | 0 |
| vpd(vpd质检标注) | `vpd质检标注_v4` | VPD_DEFAULT_REVIEWER | 1 |
| tag | 按tag_name动态 | — | — |

## 🔗 关联系统

- Delta标注平台 — 任务创建/分配/审核/验收的外部平台
- cog_fusion — 视频数据源系统
- DMP — 打回记录入库系统
- 小鹿班 — 预警通知渠道
- OBS — 审计日志存储

> ⚠️ 关联经验与规范：[[人工质检-数据库连接层]] | [[人工质检-标准文本系统]] | [[人工质检-环境配置]] | [[人工质检-状态枚举与公共定义]] | [[人工质检-数据表索引]] | [[人工质检-Delta平台API索引]]

## ⚠️ 已知架构问题

1. **代码重复**：`constant/pgserver.py` 和 `manual_label/utils/pgserver.py` 两份完全相同的PgServer+DB配置
2. **配置硬编码**：验收员列表、团队信息硬编码在 `batch_acceptance/__init__.py`
3. **新旧并存**：旧版`label_task_manage/label_mobel.py`和新版`utils/label_model.py`的LabelModel并存
4. **表名带日期**：`human_inspection_0920` 表名硬编码日期后缀
5. **手动脚本多**：分配/验收/预警/周报均为手动脚本，无统一入口
6. **监控不足**：6个DAG只有日志无看板，预警需手动触发
7. **能力散落**：分配/验收/预警/看板/周报分散在5个目录，无统一前端归口
