---
title: "人工质检-④Delta平台创建任务"
domain: ["ai_dlc", "agent_evaluation", "tooling"]
type: "concept"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_manual_qa"]
created: 2026-06-28
updated: 2026-06-28
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["人工质检-④Delta平台创建任务", "quality_check_pipeline", "manual_qa"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["4d17657f-0c07-44d2-8aef-c81d4b108fc8"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/26_Copied text 1782623323_4d17657f.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

## NotebookLM 原始元数据快照

```yaml
id: "MH-CPT-014"
title: "人工质检-④Delta平台创建任务"
domain: ["manual_qa"]
type: "concept"

related_code: ["src/data_check/manual_label/create_base.py"]

affects_path: ["src/data_check/manual_label/create_base.py", "src/data_check/manual_label/human_inspection/create_label_task.py"]
trigger_keywords: ["Delta创建任务", "send_post_request", "create_task", "addMainTask", "waitingAssign", "preLabelDataType", "entriesIds", "relationRule"]
tags: ["Delta平台", "API创建任务", "addMainTask", "waitingAssign", "e2e", "VPD", "Tag"]
summary: "通过Delta平台外部API(addMainTask)创建标注任务，任务进入waitingAssign状态等待分配。e2e/VPD/Tag三种项目类型在请求体参数上有差异(mainTaskName/dataType/preLabelDataType/entriesIds/relationRule)。"
code_hash: {}
```
# 人工质检-④Delta平台创建任务

> 通过Delta平台外部API创建标注任务，任务进入waitingAssign状态等待分配。

← [[人工质检-数据源与任务创建]] | [[人工质检-Hub]]

## 基本信息

| 维度 | 详情 |
|------|------|
| 核心代码 | `manual_label/create_base.py` → `CreatorBase.send_post_request()` / `create_task()` |
| 触发方式 | [[人工质检-③预标注与LLM决策]] 内部调用(仅who_label=0的任务) |

## Delta平台创建任务API

- **接口**：`POST https://service.di.adscloud.yinwang.com/delta/external/v1/mainTask/addMainTask`
- **认证**：Bearer token (通过 [[人工质检-Delta平台API索引]] 动态获取)
- **Headers**：
  ```
  Accept-Language: zh-cn
  Content-Type: application/json
  userName: {LABEL_OWNER}  (from env_config.yaml)
  deepdata-project: driveinsight
  deepdata-region: RaD-prod
  entrypoint-version: v2
  deepdata-platform: delta-external
  Authorization: Bearer {token}
  ```

## e2e请求体关键字段

```json
{
  "mainTaskName": "{project}_{scene_name}_{timestamp}",
  "dataSourceType": 10,
  "preLabelType": 0,
  "preLabelDataType": 22,
  "havePreLabel": 1,
  "existsGeneral": 1,
  "customInfo": {
    "dataList": [{
      "dataName": "{project}_{cfg_ver}@{clip_id}",
      "extendInfo": {
        "dataInfo": {"data_type": 0, "data_source": "autoscenes", "data_uid": "{clip_id}", "data_obs_path": "{mp4_path}"},
        "labelText": {"main_title": "驾驶行为标注", "text_items": [{"sub_answer": "{text_str}"}]}
      }
    }],
    "dataType": "AutoScenes"
  },
  "isAuto": 1,
  "labelTypeInfo": {"labelTypeId": [148]},
  "entriesIds": [370],
  "requirementInfo": {"relationRule": [relation_rule], "createTaskRule": 1}
}
```

## e2e vs VPD vs Tag 参数差异

| 参数 | e2e | VPD | Tag |
|------|-----|-----|-----|
| mainTaskName | {project}_{scene}_{ts} | 同e2e | {project}_{tag_name}_{ts} |
| dataType | AutoScenes | AutoScenes | DDI |
| preLabelDataType | 22 | 22 | 27/28/29/30 |
| entriesIds | [370] | [370] | [237] |
| relationRule | [764] | [764] | [488] |
| preLabel | 支持autochecker+LLM | 支持autochecker+LLM | 直接填tag_name |

## 其他Delta API

| API | 用途 | 详细 |
|-----|------|------|
| taskRollback | 任务回退 | → [[人工质检-Delta平台API索引]] |
| batch_assign | 批量分配 | → [[人工质检-Delta平台API索引]] |
| batchReviewPass | 批量审核通过 | → [[人工质检-Delta平台API索引]] |
| batchAcceptancePass | 批量验收通过 | → [[人工质检-Delta平台API索引]] |
| batch_delete_task | 删除waitingAssign | → [[人工质检-Delta平台API索引]] |

## 上下游

| 方向 | 关联 |
|------|------|
| 上游 | ← [[人工质检-③预标注与LLM决策]] (who_label=0的任务) |
| 下游 | → [[人工质检-⑤任务分配]] (waitingAssign状态) |

→ [[人工质检-数据源与任务创建]] | [[人工质检-Hub]]
