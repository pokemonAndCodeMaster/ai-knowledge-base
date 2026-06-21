---
title: HUB-前端与API层架构
domain: ["ai_dlc", "tooling"]
type: "hub"
tags: [质检平台, 前端, 后端API, FastAPI, Vue3, 架构总览]
created: 2026-06-21
updated: 2026-06-21
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: [前端, API, FastAPI, Vue3, QA_Brain, Web, Swagger, 单端口部署]
---

# HUB-前端与API层架构

本卡是质检一站式平台前端与后端 API 的联合架构枢纽。

## 核心部署模型

平台采用单端口部署：

- FastAPI 注册 `/api/*` 业务路由。
- FastAPI 通过 `StaticFiles` 托管 `src/frontend/dist/` 到 `/`。
- 前端 Vite 开发态通过 proxy 将 `/api` 转发到后端。
- 线上避免额外 CORS 和多服务部署复杂度。

## 现有页面分组

侧边栏使用 Element Plus `el-sub-menu` 分组，默认展开“大模型质检”。

| 路由 | 页面 | 状态 |
|---|---|---|
| `/task` | 质检任务 | 已实现：任务创建、监控、进度查看、回收站 |
| `/version` | 版本配置 | 已实现：版本参数管理 |
| `/eval` | 模型评测 | 三期骨架 |
| `/dataset` | 数据集管理 | 四期骨架 |

## 子卡导航

| 类型 | 卡片 |
|---|---|
| 后端架构 | [[FastAPI后端API层架构]] |
| 前端架构 | [[Vue3前端层架构]] |
| 任务交互 | [[TaskView交互流程详解]] |
| 版本配置交互 | [[VersionView版本配置页面交互详解]] |
| 长期架构 | [[质检一站式平台长期架构]] |
| 前端规范 | [[前端开发规范]] |

## 设计护栏

- API 路由必须保持 `/api` 前缀，静态前端挂载必须晚于 API 路由注册。
- 前端 API 调用必须通过 `src/frontend/src/api/` 封装，不允许组件直接调用 axios。
- 页面级复杂状态先用局部状态；跨页状态增长后再引入 Pinia，避免过早全局化。
- 端到端验证要覆盖前端页面 → API → 调度/数据库的真实闭环。
