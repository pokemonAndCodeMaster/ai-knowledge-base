---
title: "人工质检-⑩状态刷新与GT回写"
domain: ["ai_dlc", "agent_evaluation", "tooling"]
type: "concept"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_manual_qa"]
created: 2026-06-28
updated: 2026-06-28
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["人工质检-⑩状态刷新与GT回写", "quality_check_pipeline", "manual_qa"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["cb2918a2-a07c-474e-ae07-a5734f8eb9cd"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/32_Copied text 1782623416_cb2918a2.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

## NotebookLM 原始元数据快照

```yaml
id: "MH-CPT-020"
title: "人工质检-⑩状态刷新与GT回写"
domain: ["manual_qa"]
type: "concept"

related_code: ["src/data_check/manual_label/human_inspection/refresh_task_status.py"]

affects_path: ["src/data_check/manual_label/human_inspection/refresh_task_status.py", "src/data_check/manual_label/stand_text/*"]
trigger_keywords: ["状态刷新", "GT回写", "TaskManager", "TextParser", "GtParser", "text_gt", "event_gt", "stub", "质量表", "t_dq_e2e_label_gt"]
tags: ["状态刷新", "GT回写", "TextParser", "Stub GT", "质量表"]
summary: "同步Delta平台状态到内部表，解析标注结果为结构化GT，写入新旧质量表。6步流水线：补全→同步状态→解析GT→写旧表→写新表→确认更新。Stub DAG处理who_label=1/3/4/5的打桩GT。"
```
# 人工质检-⑩状态刷新与GT回写

> 同步Delta平台状态到内部表，解析标注结果为结构化GT，写入新旧质量表。

← [[人工质检-GT回写与中间表]] | [[人工质检-Hub]]

## 基本信息

| 维度 | 详情 |
|------|------|
| 核心代码 | `manual_label/human_inspection/refresh_task_status.py` → `TaskManager` |
| DAG | `human_inspection_refresh_status`，每30分钟 |
| Stub DAG | `human_inspection_stub_gt_save`，每30分钟 |

## 6步流水线

1. `replenish_task_info()` — 补全url/clip_id
2. `update_task_status()` — 同步DI平台状态
3. `update_task_gt()` — TextParser解析GT
4. `add_label_result_quality_table_antique()` — 写旧表`t_god_data_quality_check`
5. `add_label_result_quality_table()` — 写新表`t_dq_e2e_label_gt`(text_gt/event_gt)
6. `do_update_gt()` — 仅双表都成功才更新

## Stub GT保存

who_label=1/3/4/5的finished任务，构造打桩GT写入label_gt+质量表

## GT转换链路

```
behavior_status → TextParser.parse_all() → split_label_by_attribute()
  → text_gt + event_gt → GtParser.parse_dirty_scene()
  → save_into_dq_e2e_label_gt()
```

## 上下游

| 方向 | 关联 |
|------|------|
| 上游 | ← [[人工质检-⑨批量通过打回]] / ← [[人工质检-③预标注与LLM决策]](stub) |
| 下游 | → [[人工质检-⑪中间表更新]] |

→ [[人工质检-GT回写与中间表]] | [[人工质检-Hub]]

> 🔄 当前平台演进：[[质检平台-Delta调用与状态回查设计]] | [[质检平台-综合快照表设计]]
