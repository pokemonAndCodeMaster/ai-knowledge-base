---
title: "VersionView版本配置页面交互详解"
domain: ["ai_dlc", "tooling"]
type: "module_doc"
tags: ["quality_check_pipeline", "NotebookLM", "完整摄入", "原业务域_common_infra"]
created: 2026-06-28
updated: 2026-06-28
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["VersionView版本配置页面交互详解", "quality_check_pipeline", "common_infra"]
notebook_id: "fc03a900-e886-44a5-85b0-73983c0efa41"
source_ids: ["30ebcb30-c85a-47c1-9839-e75a322942ec"]
raw_sources: ["raw/notebooklm_exports/fc03a900-e886-44a5-85b0-73983c0efa41/05_Copied text 1781950532_30ebcb30.md"]
---

> [!NOTE] 来源范围与完整性
> 本卡正文完整保留自 NotebookLM `quality_check_pipeline`。原文描述的是上游 `e2e_data_pipeline_hub` 快照；其中路径/API 不自动等同于当前仓库实现。原始字节与 SHA-256 见 [[notebooklm_quality_check_pipeline]]。

## NotebookLM 原始元数据快照

```yaml
id: "MOD-FE-002"
title: "VersionView版本配置页面交互详解"
domain: ["common_infra"]
type: "module_doc"

related_code: ["src/frontend/src/views/VersionView.vue", "src/frontend/src/api/version.ts", "src/frontend/src/utils/jsonFormatter.ts"]
affects_path: ["src/frontend/src/views/VersionView.vue"]
trigger_keywords: ["VersionView", "版本配置", "CRUD", "创建配置", "编辑配置", "删除配置", "JSONB", "通道筛选"]
tags: ["VersionView", "版本配置", "CRUD", "JSONB"]
summary: "VersionView.vue 的完整 CRUD 交互流程：通道筛选(model/video/prompt)、创建/编辑对话框(JSON输入+校验)、详情查看(JSONB格式化)、删除确认、OFFSET分页。"
```
# VersionView 版本配置页面交互详解

## 页面加载流程

```
onMounted()
  └── fetchConfigs()   → GET /api/versions/?limit=20&offset=0
      └── 更新 configList + totalConfigs
```

## 顶部操作栏

| 控件 | 行为 |
|------|------|
| `el-select` (通道筛选) | `filterChannel` → change → `fetchConfigs()` |
| "创建新配置"按钮 | → `openCreateDialog()` |
| "刷新"按钮 | → `fetchConfigs()` |

通道选项：model / video / prompt

## 配置列表 (el-table)

| 列 | 字段 | 说明 |
|----|------|------|
| 版本号 | `version` | width=200, overflow-tooltip |
| 通道 | `channel` | `el-tag` 展示 |
| 处理器 | `processor` | width=160, overflow-tooltip |
| 创建时间 | `created_at` | width=180 |
| 更新时间 | `updated_at` | width=180 |
| 操作 | - | 查看/编辑/删除 |

### 分页 (el-pagination)

- `page-sizes=[10,20,50,100]`，`pageSize` 默认 20
- OFFSET 分页：`offset = (currentPage - 1) * pageSize`
- 筛选参数：`version` / `channel`

## 创建/编辑对话框

`el-dialog` 标题动态切换：创建/编辑版本配置

### 表单字段

| 字段 | 控件 | 必填 | 编辑时 |
|------|------|------|--------|
| 版本号 | `el-input` | ✅ | disabled |
| 通道 | `el-select` (model/video/prompt) | ✅ | disabled |
| 配置 (JSON) | `el-input type="textarea" :rows="6"` | ✅ | 可编辑 |
| 处理器 | `el-input` | 可选 | 可编辑 |
| 处理器参数 (JSON) | `el-input type="textarea" :rows="4"` | 可选 | 可编辑 |

### JSON 校验规则

```typescript
formRules: {
  configStr: [
    { required: true, message: '请输入配置内容' },
    {
      validator: (_rule, value, callback) => {
        try { JSON.parse(value); callback() }
        catch { callback(new Error('配置必须为合法 JSON')) }
      },
      trigger: 'blur',
    },
  ],
}
```

### 提交流程

```
handleSubmit()
  ├── formRef.validate()      → 校验表单
  ├── JSON.parse(configStr)   → 解析配置 JSON
  ├── JSON.parse(processorParamsStr) → 解析处理器参数 JSON（可选）
  └── createVersionConfig({ version, channel, config, processor, processor_params })
      → POST /api/versions/
      → UPSERT：version+channel 已存在则更新
```

**关键**：编辑和创建使用同一个 API（后端 UPSERT 语义），版本号+通道作为联合键。

## 详情对话框

```
showDetail(row) → getVersionConfigDetail(version, channel)
  → GET /api/versions/detail?version=X&channel=Y
  → el-descriptions 展示
```

| 展示项 | 说明 |
|--------|------|
| 版本号 | 文本 |
| 通道 | 文本 |
| 配置 | JSONB → `formatJsonBToText()` 格式化展示 |
| 处理器 | 文本或"无" |
| 处理器参数 | JSONB → `formatJsonBToText()` 格式化展示 |
| 创建时间 | 文本 |
| 更新时间 | 文本 |

## 删除操作

```
handleDelete(row)
  → ElMessageBox.confirm("确认删除? 此操作不可恢复", type='error')
  → deleteVersionConfig(version, channel)
    → DELETE /api/versions/{version}/{channel}
  → 成功 → fetchConfigs() 刷新列表
```

## API 函数映射

| 前端函数 | 后端端点 |
|----------|----------|
| `createVersionConfig` | POST `/versions/` |
| `getVersionConfigs` | GET `/versions/` |
| `getVersionConfigDetail` | GET `/versions/detail` |
| `deleteVersionConfig` | DELETE `/versions/{version}/{channel}` |

> ⚠️ 关联经验与规范：[[HUB-前端与API层架构]]、[[Vue3前端层架构]]、[[FastAPI后端API层架构]]
