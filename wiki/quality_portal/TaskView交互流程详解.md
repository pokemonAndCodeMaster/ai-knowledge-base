---
title: TaskView交互流程详解
domain: ["ai_dlc", "tooling"]
type: "module_doc"
tags: [质检平台, TaskView, 交互流程, 分组概览, 回收站, CRUD, 游标分页]
created: 2026-06-21
updated: 2026-06-21
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: [TaskView, 任务列表, 任务组, 分组概览, 展开折叠, 通道圆点, 回收站, 批量清理, 游标分页, 版本详情弹窗]
---

# TaskView交互流程详解

`TaskView.vue` 是质检任务运营主页面，负责任务组概览、组内任务下钻、任务创建、回收站和批量清理。

## 页面加载模型

- 不再使用 `overview + list` 双请求模式。
- 默认使用任务组概览单请求。
- 展开某个任务组时，再懒加载组内子任务。

Tab：

- `activeTab === "tasks"`：任务组概览 + 展开子任务。
- `activeTab === "recycle"`：回收站组件 `RecycleBinTab`。

## 任务组概览

顶部 6 张统计卡片来自 `groupStatusSummary`：

- 总任务组数
- 待处理
- 运行中
- 已完成
- 失败
- 已取消

工具栏：

- “创建任务” → `showCreateDialog = true`
- “刷新” → `fetchGroups()`
- “批量清理” → `selectedIds.size > 0` 时可用，触发 `handleBatchClean()`

## 两级加载

`displayedRows` 将 `groupsData.groups` 转为 `GroupDisplayRow`，展开时插入子任务行。

组行字段包括：

- `taskName`
- `total/pending/running/completed/failed/cancelled`
- `raw_img_progress` 至 `inference_progress`
- `data/label/pkl/video_config/prompt/model_version`
- `latest_created_at`

点击组名：

1. `toggleGroupExpand(groupKey)`
2. 提取 `task_name`
3. 同一时间最多展开一个组
4. `loadExpandedTasks(taskName)`
5. 调用 `GET /api/tasks/list?task_name_exact=XXX&limit=50`

子任务行展示单任务详情，包括 6 通道状态圆点和 6 个版本链接。

## 组内分页

展开某组后使用“加载更多”：

- 首页：`getTaskList({ task_name_exact, limit })`
- 下一页：`getTaskList({ task_name_exact, limit, cursor: next_cursor })`
- 返回结构：`items + next_cursor + has_more`
- 无 `prev_cursor`，只支持向前加载。

## 回收站

`RecycleBinTab` 查询 `getTaskList({ is_deleted: "true", limit, cursor })`。

操作：

- “恢复” → `restoreTask(id)` → `POST /api/tasks/{id}/restore` → `emit("data-changed")`
- “永久删除” → 二次确认 → `permanentDeleteTask(id)` → `POST /api/tasks/{id}/permanent-delete`

## 创建任务

弹窗使用 `el-tabs`：

- 表单创建：必填 `task_name`、`autosence_id`；版本字段直接输入。
- 文件上传：`.json/.jsonl`，`auto-upload=false`，提交时用 multipart 上传。

错误处理：

- API 层 axios 拦截器统一弹出 `ElMessage.error()`。
- 页面隐藏时错误进入队列，恢复可见后再弹出。
- 视图层 `catch` 不重复处理通用错误。

> 关联经验与规范：[[HUB-前端与API层架构]]、[[Vue3前端层架构]]、[[FastAPI后端API层架构]]
