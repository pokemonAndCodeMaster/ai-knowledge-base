---
title: "人工质检-GT回写与中间表"
domain: ["ai_dlc", "agent_evaluation", "tooling"]
type: "concept"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_manual_qa", "原业务域_common_infra"]
created: 2026-06-28
updated: 2026-06-28
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["人工质检-GT回写与中间表", "quality_check_pipeline", "manual_qa", "common_infra"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["46d71273-d9bd-45c6-8e55-c6f8f2a3e1d3"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/21_Copied text 1782623261_46d71273.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

## NotebookLM 原始元数据快照

```yaml
id: "MH-CPT-013"
title: "人工质检-GT回写与中间表"
domain: ["manual_qa", "common_infra"]
type: "concept"

related_code: ["src/data_check/manual_label/human_inspection/refresh_task_status.py", "src/data_check/manual_label/middleware_table_process/process_middleware_table.py", "src/data_check/manual_label/delete_duplicate_records.py", "src/data_check/manual_label/middleware_table_process/obs_log_writer.py"]

affects_path: ["src/data_check/manual_label/human_inspection/refresh_task_status.py", "src/data_check/manual_label/middleware_table_process/*", "src/data_check/manual_label/delete_duplicate_records.py"]
trigger_keywords: ["GT回写", "中间表", "状态刷新", "TaskManager", "去重", "OBS审计", "t_dq_e2e_label_gt", "TextParser", "GtParser"]
tags: ["GT回写", "中间表", "去重", "OBS审计", "数据转换"]
summary: "标注结果解析为结构化GT入库(Delta JSON→TextParser→GtParser→t_dq_e2e_label_gt)，中间表供看板/报表消费，重复数据自动清理(IOU重叠)，OBS审计日志全程记录。"
```
# 人工质检-GT回写与中间表

> 标注结果解析为结构化GT入库，中间表供看板/报表消费，重复数据自动清理。

← [[人工质检-Hub]]

## 步骤清单

| 步骤 | 名称 | 核心代码 | DAG | 详细卡片 |
|------|------|---------|-----|---------|
| ⑩ | 状态刷新+GT回写 | `human_inspection/refresh_task_status.py` → `TaskManager` | `human_inspection_refresh_status`(30min) | [[人工质检-⑩状态刷新与GT回写]] |
| ⑪ | 中间表更新 | `middleware_table_process/process_middleware_table.py` → `update_middleware()` | `human_inspection_update_middleware`(6h) | [[人工质检-⑪中间表更新]] |
| ⑭ | 重复数据清理 | `delete_duplicate_records.py` → `batch_dedup_and_clean()` | 入库前自动+手动 | [[人工质检-⑭重复数据清理]] |
| ⑮ | OBS审计日志 | `middleware_table_process/obs_log_writer.py` → `LocalLogWriter` | 所有入库操作自动 | [[人工质检-⑮OBS审计日志]] |

## GT转换链路

```
Delta标注JSON(behavior_status)
  → TextParser.parse_all() → all_gts + idx2attribute
  → split_label_by_attribute() → text_gt(驾驶行为) + event_gt(场景分类)
  → GtParser.parse_dirty_scene() → 中英文key映射
  → save_into_dq_e2e_label_gt() → INSERT/UPDATE t_dq_e2e_label_gt
```

## 新旧质量表对比

| 维度 | 旧表 `t_god_data_quality_check` | 新表 `t_dq_e2e_label_gt` |
|------|------|------|
| 主键 | autoscenes_id | (ide_task_id, autoscenes_id) |
| GT存储 | 单个human_check JSONB | text_gt + event_gt + construction_gt |
| 去重 | 无 | IOU区间重叠检查 |
| 项目区分 | E2E/VPD分表 | 单表project_name区分 |

→ [[人工质检-Hub]] | [[人工质检-验收与通过打回]] | [[人工质检-预警与报表]]

> ⚠️ 关联经验与规范：[[人工质检-⑩状态刷新与GT回写]] | [[人工质检-⑪中间表更新]] | [[人工质检-⑭重复数据清理]] | [[人工质检-⑮OBS审计日志]]
