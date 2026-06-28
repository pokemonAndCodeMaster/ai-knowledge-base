---
title: "HUB-前端与API层架构"
domain: ["ai_dlc", "tooling"]
type: "hub"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_common_infra"]
created: 2026-06-28
updated: 2026-06-28
sources: 2
status: active
related_code: []
affects_path: []
trigger_keywords: ["HUB-前端与API层架构", "quality_check_pipeline", "common_infra"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["bcb6fe6e-53bd-4f8c-9ed1-bd1569ac5f91", "7f449783-b4e1-4544-8d8f-4e8f194b89db"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/02_Copied text 1781950450_bcb6fe6e.md", "raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/15_Copied text 1782623137_7f449783.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

> NotebookLM 中存在 2 份字节级重复 source；本卡合并编纂，原始文件均独立保留。

## NotebookLM 原始元数据快照

```yaml
id: "HUB-FE-API-001"
title: "HUB-前端与API层架构"
domain: ["common_infra"]
type: "hub"

related_code: ["src/api/", "src/frontend/"]
affects_path: ["src/api/app.py", "src/api/deps.py", "src/frontend/package.json", "src/frontend/vite.config.ts"]
trigger_keywords: ["前端", "API", "FastAPI", "Vue3", "QA Brain", "Web", "Swagger"]
tags: ["前端", "后端API", "架构总览", "FastAPI", "Vue3"]
summary: "前端(Vue3+ElementPlus)与后端(FastAPI)的联合架构枢纽卡。单端口部署：FastAPI 提供API路由 + StaticFiles 托管前端 dist。导航至环境配置、启动调试、后端架构、前端架构、交互流程等子卡片。"
```
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
