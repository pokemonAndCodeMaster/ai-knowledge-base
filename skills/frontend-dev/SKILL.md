---
name: frontend-dev
description: |
  前端开发辅助 Skill。在处理 src/frontend/ 下的代码创建、修改、Review 时自动激活。
  强制执行前端开发规范，提供 Vue 3 + TypeScript + Element Plus 代码模板，
  确保新代码符合架构设计和编码约定。
trigger_keywords:
  - 前端
  - Vue
  - 组件
  - 页面
  - Element Plus
  - 表格
  - 表单
  - 路由
  - API 对接
---

# 🔧 前端开发辅助 Skill

## 何时触发

当用户请求涉及以下场景时，必须激活本 Skill：
1. 在 `src/frontend/` 下创建或修改 `.vue`、`.ts` 文件
2. 新增业务模块、页面、组件
3. 对接后端 API（创建 `api/` 层函数）
4. 进行前端 Code Review

## 前置检查

在生成任何前端代码前，必须确认已阅读以下知识卡片：
- [[数据质量门户架构设计]] — 目录结构和扩展规范
- [[前端开发规范]] — 命名规范和编码约定

## 强制规则

以下规则在生成代码时**必须遵守**，违反任何一条即为不合格输出：

### R1：文件放置
```
新页面 → src/frontend/src/views/<模块名>/
新组件（单模块用）→ 和页面同目录
新组件（跨模块用）→ src/frontend/src/components/
新 API 函数 → src/frontend/src/api/<模块名>.ts
新类型定义 → src/frontend/src/types/<模块名>.ts
```

### R2：命名规范
```
Vue 文件名 → PascalCase（如 TaskList.vue）
TS 文件名 → camelCase（如 llmQc.ts）
目录名 → kebab-case（如 llm-qc/）
变量/函数 → camelCase
类型/接口 → PascalCase
CSS 类名 → kebab-case
```

### R3：组件结构
```
顺序固定为：<template> → <script setup lang="ts"> → <style scoped>
script 内部顺序：导入 → Props/Emits → 响应式数据 → 计算属性 → 方法 → 生命周期
```

### R4：禁止事项
```
❌ 使用 any 类型
❌ 模板中写复杂表达式（超过一行的逻辑必须提取为 computed）
❌ 硬编码颜色值（必须用 CSS 变量）
❌ <style> 不加 scoped
❌ 组件中直接使用 axios（必须通过 api/ 层）
❌ v-for 不加 :key
❌ console.log 残留
```

## 代码模板

### 新页面模板

```vue
<template>
  <div class="page-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>{{ pageTitle }}</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新建
      </el-button>
    </div>

    <!-- 搜索条件 -->
    <el-form :model="searchForm" inline class="search-form">
      <el-form-item label="名称">
        <el-input v-model="searchForm.name" placeholder="请输入" clearable />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="searchForm.status" placeholder="全部" clearable>
          <el-option label="等待中" value="pending" />
          <el-option label="运行中" value="running" />
          <el-option label="已完成" value="completed" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="loadData">查询</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 数据表格 -->
    <el-table :data="tableData" v-loading="loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="名称" />
      <el-table-column label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleView(row)">查看</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="page"
      :total="total"
      :page-size="pageSize"
      layout="total, prev, pager, next"
      @current-change="loadData"
      class="pagination"
    />
  </div>
</template>

<script setup lang="ts">
// ═══════════════════════════════════════
// ① 导入
// ═══════════════════════════════════════
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// TODO: 替换为实际的 API 和类型导入
// import { getList, deleteItem } from '@/api/moduleName'
// import type { ItemType } from '@/types/moduleName'

// ═══════════════════════════════════════
// ② 响应式数据
// ═══════════════════════════════════════
const router = useRouter()
const loading = ref(false)
const tableData = ref<any[]>([])  // TODO: 替换 any 为具体类型
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const pageTitle = '页面标题'  // TODO: 修改

const searchForm = ref({
  name: '',
  status: '',
})

// ═══════════════════════════════════════
// ③ 方法
// ═══════════════════════════════════════
function statusType(status: string) {
  const map: Record<string, string> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
  }
  return map[status] || 'info'
}

async function loadData() {
  loading.value = true
  try {
    // TODO: 替换为实际 API 调用
    // const result = await getList({ page: page.value, size: pageSize.value, ...searchForm.value })
    // tableData.value = result.items
    // total.value = result.total
  } finally {
    loading.value = false
  }
}

function resetSearch() {
  searchForm.value = { name: '', status: '' }
  page.value = 1
  loadData()
}

function handleCreate() {
  // TODO: 打开新建弹窗或跳转
}

function handleView(row: any) {
  // TODO: 跳转到详情页
  // router.push(`/module/${row.id}`)
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('确认删除？', '提示', { type: 'warning' })
  // TODO: await deleteItem(id)
  ElMessage.success('删除成功')
  loadData()
}

// ═══════════════════════════════════════
// ④ 生命周期
// ═══════════════════════════════════════
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-container {
  padding: var(--spacing-lg);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.search-form {
  margin-bottom: var(--spacing-md);
}

.pagination {
  margin-top: var(--spacing-md);
  justify-content: flex-end;
}
</style>
```

### 新 API 文件模板

```typescript
// api/<moduleName>.ts
import request from './request'
import type { PageResult } from '@/types/common'
// import type { XxxItem } from '@/types/<moduleName>'

// ═══════════════════════════════════════
// 列表查询
// ═══════════════════════════════════════
export function getXxxList(params: {
  page: number
  size: number
  name?: string
  status?: string
}) {
  return request.get<any, PageResult<any>>('/api/v1/<module>/items', { params })
  // TODO: 替换 any 为具体类型
}

// ═══════════════════════════════════════
// 详情查询
// ═══════════════════════════════════════
export function getXxxDetail(id: number) {
  return request.get(`/api/v1/<module>/items/${id}`)
}

// ═══════════════════════════════════════
// 创建
// ═══════════════════════════════════════
export function createXxx(data: any) {
  return request.post('/api/v1/<module>/items', data)
  // TODO: 替换 any 为 CreateXxxParams
}

// ═══════════════════════════════════════
// 更新
// ═══════════════════════════════════════
export function updateXxx(id: number, data: any) {
  return request.put(`/api/v1/<module>/items/${id}`, data)
}

// ═══════════════════════════════════════
// 删除
// ═══════════════════════════════════════
export function deleteXxx(id: number) {
  return request.delete(`/api/v1/<module>/items/${id}`)
}
```

### 新类型文件模板

```typescript
// types/<moduleName>.ts

/**
 * <描述> 列表项类型
 */
export interface XxxItem {
  id: number
  name: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  created_at: string
  updated_at: string
}

/**
 * 创建参数（去掉 id 和时间戳）
 */
export type CreateXxxParams = Omit<XxxItem, 'id' | 'created_at' | 'updated_at'>

/**
 * 更新参数（全部可选）
 */
export type UpdateXxxParams = Partial<CreateXxxParams>
```

## Review 检查清单

生成代码后，必须对照以下清单自检：

- [ ] 文件放在正确目录
- [ ] 命名符合规范（PascalCase/camelCase/kebab-case）
- [ ] `<style scoped>` 已添加
- [ ] template → script → style 顺序
- [ ] 无 `any` 类型（模板代码中的 TODO 除外）
- [ ] 无硬编码颜色值
- [ ] 无 `console.log`
- [ ] `v-for` 有 `:key`
- [ ] API 通过 `api/` 层调用
- [ ] 必要的类型定义在 `types/` 中
