---
title: VersionView版本配置页面交互详解
domain: ["ai_dlc", "tooling"]
type: "module_doc"
tags: [质检平台, VersionView, 版本配置, CRUD, JSONB, OFFSET分页]
created: 2026-06-21
updated: 2026-06-21
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: [VersionView, 版本配置, CRUD, 创建配置, 编辑配置, 删除配置, JSONB, 通道筛选]
---

# VersionView版本配置页面交互详解

`VersionView.vue` 管理模型、视频、Prompt 等版本配置，是 LLM 任务调度 Pipeline 的配置入口之一。

## 页面控件

- 通道筛选：`filterChannel` 变化后调用 `fetchConfigs()`。
- “创建新配置” → `openCreateDialog()`。
- “刷新” → `fetchConfigs()`。

通道选项：

- `model`
- `video`
- `prompt`

## 列表与分页

表格列：

- 版本号 `version`
- 通道 `channel`
- 处理器 `processor`
- 创建时间 `created_at`
- 更新时间 `updated_at`
- 操作：查看 / 编辑 / 删除

分页使用 OFFSET：

- `pageSize` 默认 20。
- `offset = (currentPage - 1) * pageSize`。
- 支持 `version` / `channel` 筛选。

## 创建与编辑

创建和编辑共用同一对话框。

字段：

- `version`：必填，编辑时禁用。
- `channel`：必填，编辑时禁用。
- `config`：JSON，必填。
- `processor`：可选。
- `processor_params`：JSON，可选。

创建/编辑使用同一个 API，后端采用 UPSERT 语义，`version + channel` 是联合键。

## 详情与删除

详情对话框展示：

- 版本号
- 通道
- `config` JSONB，经 `formatJsonBToText()` 格式化
- 处理器
- `processor_params` JSONB，经 `formatJsonBToText()` 格式化
- 创建时间
- 更新时间

删除走 `DELETE /versions/{version}/{channel}`，必须保留确认。

## API 映射

| 前端函数 | 后端端点 |
|---|---|
| `createVersionConfig` | `POST /versions/` |
| `getVersionConfigs` | `GET /versions/` |
| `getVersionConfigDetail` | `GET /versions/detail` |
| `deleteVersionConfig` | `DELETE /versions/{version}/{channel}` |

> 关联经验与规范：[[HUB-前端与API层架构]]、[[Vue3前端层架构]]、[[FastAPI后端API层架构]]、[[LLM任务调度Pipeline全景]]
