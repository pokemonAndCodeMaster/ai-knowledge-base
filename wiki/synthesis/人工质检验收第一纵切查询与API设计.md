---
title: "人工质检验收第一纵切查询与API设计"
domain: ["ai_dlc", "tooling"]
type: "synthesis"
tags: ["人工质检", "验收", "API", "QuerySpec", "聚合查询"]
created: 2026-07-05
updated: 2026-07-06
sources: 7
status: active
related_code: ["src/api/schemas/acceptance.py", "src/manual_qc/repository.py", "src/manual_qc/acceptance/"]
affects_path: ["src/api/schemas/acceptance.py", "src/manual_qc/repository.py", "src/manual_qc/acceptance/"]
trigger_keywords: ["验收查询API", "QuerySpec", "任务聚合API", "按日展开API"]
---

# 人工质检验收第一纵切查询与 API 设计

← [[人工质检验收第一纵切架构枢纽]]。

## API

```text
POST /api/v1/manual-qc/acceptance/tasks/query
GET  /api/v1/manual-qc/acceptance/tasks/{task_id}/breakdown?dimension=date
GET  /api/v1/manual-qc/acceptance/metadata
POST /api/v1/manual-qc/acceptance/assignment/preview
GET  /api/v1/manual-qc/acceptance/assignment/previews/{preview_id}
GET/POST /api/v1/ui/views
```

`QuerySpec` 包含 filters、sorting、page、page_size。过滤字段必须经过后端白名单映射，不能把客户端字段名直接拼入 SQL。响应返回 items、total、page、page_size 和 computed_at。

任务聚合从交付任务左连接快照，以任务为一行；`recent_annotation_days` 只返回最近若干个 `annotation_submitted > 0` 的日期。breakdown 首版实现 `date`，接口保留 `group/annotator/scene` 枚举但未实现时返回明确错误。

分配 preview 使用 [[人工质检验收分配预览闭环设计]] 的 `SelectionSpec + AssignmentRuleSpec`。POST 返回 preview_id、source_version、过期时间、总量、Good/Bad 计划、缺口、警告和日期明细；GET 只允许创建人读取仍为 READY 且未过期的预览。

## 错误契约

- 不支持字段/操作符：422；
- 任务不存在：404；
- 未实现展开维度：400 + 稳定错误码；
- 数据库失败：统一 500，日志保留查询上下文但不泄漏 SQL 密钥。
- 选择为空、ID 非法或维度未实现：422 + `INVALID_SELECTION`；
- 预览不存在、非创建人或已过期：404 + `PREVIEW_NOT_FOUND_OR_EXPIRED`。
