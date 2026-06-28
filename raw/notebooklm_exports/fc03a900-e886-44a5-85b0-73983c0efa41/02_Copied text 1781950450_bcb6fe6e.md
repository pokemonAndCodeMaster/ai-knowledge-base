---
id: "HUB-FE-API-001"
title: "HUB-前端与API层架构"
domain: ["common_infra"]
type: "hub"

related_code: ["src/api/", "src/frontend/"]
affects_path: ["src/api/app.py", "src/api/deps.py", "src/frontend/package.json", "src/frontend/vite.config.ts"]
trigger_keywords: ["前端", "API", "FastAPI", "Vue3", "QA Brain", "Web", "Swagger"]
tags: ["前端", "后端API", "架构总览", "FastAPI", "Vue3"]
summary: "前端(Vue3+ElementPlus)与后端(FastAPI)的联合架构枢纽卡。单端口部署：FastAPI 提供API路由 + StaticFiles 托管前端 dist。导航至环境配置、启动调试、后端架构、前端架构、交互流程等子卡片。"
---

# 前端与API层架构 (HUB)

## 整体架构

```
┌──────────────────────────────────────────────┐
│  浏览器 (http://localhost:8000)               │
│  ├─ /api/*    → FastAPI 路由 (JSON API)       │
│  └─ /*        → StaticFiles (frontend/dist)   │
└──────────────────────────────────────────────┘
        │                    │
        ▼                    ▼
┌──────────────┐  ┌──────────────────┐
│ FastAPI 后端  │  │ Vue3 前端 (dist/) │
│ :8000 单端口  │  │ ElementPlus UI   │
└──────────────┘  └──────────────────┘
```

**核心设计**：单端口部署，FastAPI 的 `StaticFiles` 中间件将 `src/frontend/dist/` 挂载到 `/`，API 路由注册在 `/api/` 前缀下。前端 Vite 开发时通过 `proxy` 代理 `/api` 到后端。

## 侧边栏结构

```
┌────────────────┐
│    QA Brain    │
│ ──────────── │
│ ▼ 大模型质检   │
│   质检任务     │ ← /task
│   版本配置     │ ← /version
│   模型评测     │ ← /eval
│   数据集管理   │ ← /dataset
└────────────────┘
```

侧边栏使用 `el-sub-menu` 实现分组，"大模型质检" 为默认展开的分组，4 个子页签均可点击导航。

## 模块导航

| 子卡片 | 类型 | 导航 |
|--------|------|------|
| 环境配置 | norm | [[前端与API环境配置指南]] |
| 启动调试 | norm | [[前端与API启动调试指南]] |
| 后端架构 | code_module | [[FastAPI后端API层架构]] |
| 前端架构 | code_module | [[Vue3前端层架构]] |
| 任务交互 | module_doc | [[TaskView交互流程详解]] |
| 版本配置交互 | module_doc | [[VersionView版本配置页面交互详解]] |
| 常见排错 | pitfall | [[前端常见问题与排错指南]] |

## 开发阶段

| 模块 | 状态 | 说明 |
|------|------|------|
| 质检任务 | ✅ 已实现 | 完整 CRUD + 文件上传 + 任务组概览 + 回收站 |
| 版本配置 | ✅ 已实现 | 完整 CRUD (创建/列表/详情/编辑/删除) |
| 模型评测 | 🔧 三期骨架 | API 骨架已注册，前端占位 |
| 数据集管理 | 🔧 四期骨架 | API 骨架已注册，前端占位 |

> ⚠️ 关联经验与规范：[[前端与API环境配置指南]]、[[前端与API启动调试指南]]、[[前端常见问题与排错指南]]
