---
title: "人工质检-⑮OBS审计日志"
domain: ["ai_dlc", "agent_evaluation", "tooling"]
type: "concept"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_manual_qa", "原业务域_common_infra"]
created: 2026-06-28
updated: 2026-06-28
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["人工质检-⑮OBS审计日志", "quality_check_pipeline", "manual_qa", "common_infra"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["c318f271-055d-4fe7-a17c-01544159bca0"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/37_Copied text 1782623471_c318f271.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

## NotebookLM 原始元数据快照

```yaml
id: "MH-CPT-023"
title: "人工质检-⑮OBS审计日志"
domain: ["manual_qa", "common_infra"]
type: "concept"

related_code: ["src/data_check/manual_label/middleware_table_process/obs_log_writer.py"]

affects_path: ["src/data_check/manual_label/middleware_table_process/obs_log_writer.py"]
trigger_keywords: ["OBS审计", "审计日志", "obs_log_writer", "LocalLogWriter", "jsonl", "HUMAN_CHECK_RUN_TS"]
tags: ["审计", "OBS", "日志", "入库追踪"]
summary: "所有入库操作的审计日志，写入本地JSONL+上传OBS，线程安全，排他创建，支持success/fail/skip/delete四种事件。"
```
# 人工质检-⑮OBS审计日志

> 所有入库操作的审计日志，写入本地JSONL+上传OBS。

← [[人工质检-GT回写与中间表]] | [[人工质检-Hub]]

## 基本信息

| 维度 | 详情 |
|------|------|
| 核心代码 | `manual_label/middleware_table_process/obs_log_writer.py` → `LocalLogWriter` |
| 触发方式 | 所有入库操作自动调用 |

## 存储路径

本地：/tmp/human_check/insert_into_gt/{YYYY-MM-DD}/{子目录}/{HH_MM_SS}/{batch_id}.jsonl
OBS：obs://yw-ads-training-gy1/data/external/personal/l00886034/human_check/...

## 子目录规则

save_into_quality_check → quality_check/
save_into_quality_check_vpd → quality_check_vpd/
其他 → dq_e2e_label_gt/

## 事件类型

log_success() / log_fail() / log_skip() / log_delete()
首行summary：{total, success, fail, skip, delete}

特性：线程安全(Lock) / 排他创建(O_CREAT|O_EXCL) / HUMAN_CHECK_RUN_TS环境变量

→ [[人工质检-GT回写与中间表]] | [[人工质检-Hub]]
