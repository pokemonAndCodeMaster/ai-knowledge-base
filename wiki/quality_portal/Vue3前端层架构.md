---
title: Vue3前端层架构
domain: ["ai_dlc", "tooling"]
type: "module_doc"
tags: [质检平台, Vue3, 前端架构, ElementPlus, Vite, TypeScript, 路由, HTTP封装]
created: 2026-06-21
updated: 2026-06-21
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: [Vue3, 前端, ElementPlus, Vite, axios, router, 侧边栏, MainLayout, RecycleBinTab, VersionDetailDialog]
---

# Vue3前端层架构

Vue3 前端层用于承载质检任务运营界面。当前技术栈是 Vue3 + TypeScript + Vite + Element Plus。

## 关键文件职责

| 文件 | 职责 |
|---|---|
| `src/frontend/src/main.ts` | 应用入口 |
| `src/frontend/src/router/index.ts` | Vue Router 路由定义，使用 HTML5 History 模式 |
| `src/frontend/src/layouts/MainLayout.vue` | 侧边栏与主内容布局 |
| `src/frontend/src/api/index.ts` | axios HTTP 封装与统一错误处理 |
| `src/frontend/src/api/task.ts` | 质检任务 API 函数 |
| `src/frontend/src/api/version.ts` | 版本配置 API 函数 |
| `src/frontend/src/views/TaskView.vue` | 质检任务页面 |
| `src/frontend/src/views/VersionView.vue` | 版本配置页面 |
| `src/frontend/src/components/RecycleBinTab.vue` | 回收站组件 |
| `src/frontend/src/components/VersionDetailDialog.vue` | 版本详情弹窗 |

## 路由与布局

- `router/index.ts` 默认重定向到 `/task`。
- 子路由使用懒加载：`() => import('../views/XxxView.vue')`。
- `MainLayout.vue` 使用 `el-aside` + `el-menu` 构建侧边栏。
- 侧边栏使用 `el-sub-menu` 分组，默认展开大模型质检分组。
- `activeMenu = computed(() => route.path)` 保持当前页签高亮。

## API 封装规则

- 组件不得直接使用 axios，必须通过 `api/` 层函数。
- `api/index.ts` 统一处理错误提示。
- `visibilityState` 守卫用于避免浏览器后台期间错误弹窗堆积：后台错误进入队列，页面恢复可见后以 200ms 间隔逐条弹出。
- 视图层 `catch` 不重复弹错误，只处理业务特定分支。

## 已有 API 函数

任务 API：

- `createTaskByForm` → `POST /tasks/create`
- `createTaskByFile` → `POST /tasks/upload`
- `getTaskOverview` → `GET /tasks/overview`
- `fetchTaskGroups` → `GET /tasks/groups`
- `getTaskList` → `GET /tasks/list`
- `getTaskDetail` → `GET /tasks/{id}`
- `getChannelProgress` → `GET /tasks/channel/progress`
- `getChannelThroughput` → `GET /tasks/channel/throughput`
- `cleanTask` → `POST /tasks/{id}/clean`
- `batchCleanTasks` → `POST /tasks/batch-clean`
- `restoreTask` → `POST /tasks/{id}/restore`
- `permanentDeleteTask` → `POST /tasks/{id}/permanent-delete`

版本 API：

- `createVersionConfig` → `POST /versions/`
- `getVersionConfigs` → `GET /versions/`
- `getVersionConfigDetail` → `GET /versions/detail`
- `deleteVersionConfig` → `DELETE /versions/{version}/{channel}`

## 长期扩展提示

- 当前两页签下，局部状态和组件事件足够。
- 当模型评测、数据集管理与任务列表出现跨页联动时，应引入 Pinia 管理跨模块状态。
- `vue-tsc` 失败会中断 `npm run build`，新增代码必须减少 `any` 和隐式类型债务。

> 关联经验与规范：[[前端开发规范]]、[[HUB-前端与API层架构]]、[[TaskView交互流程详解]]、[[VersionView版本配置页面交互详解]]
