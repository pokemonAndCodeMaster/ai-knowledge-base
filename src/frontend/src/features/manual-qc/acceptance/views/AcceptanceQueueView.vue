<script setup lang="ts">
import { computed, onMounted, shallowRef } from 'vue'

import DataWorkbench from '@/shared/data-workbench/DataWorkbench.vue'
import type { WorkbenchRow } from '@/shared/data-workbench/types'
import DashboardLayout from '@/shared/dashboard/DashboardLayout.vue'
import type { DashboardCardConfig } from '@/shared/dashboard/types'

import { getAcceptanceDailyBreakdown, queryAcceptanceTasks } from '../api'
import { acceptanceColumns } from '../columns'
import AssignmentPreviewPanel from '../components/AssignmentPreviewPanel.vue'
import { useAssignmentPreview } from '../composables/useAssignmentPreview'
import type { AcceptanceTask, QuerySpec } from '../types'

const rows = shallowRef<AcceptanceTask[]>([])
const loading = shallowRef(false)
const error = shallowRef('')
const computedAt = shallowRef('')
const editLayout = shallowRef(false)
const {
  preview,
  loading: previewLoading,
  error: previewError,
  visible: previewVisible,
  generate: generatePreview,
  invalidate: invalidatePreview,
  handleSelectionChange,
} = useAssignmentPreview()

const summary = computed(() => ({
  tasks: rows.value.length,
  submitted: rows.value.reduce((sum, item) => sum + item.annotation_submitted, 0),
  allocated: rows.value.reduce((sum, item) => sum + item.acceptance_allocated, 0),
  pending: rows.value.filter(item => item.acceptance_allocated === 0).length,
}))

const summaryCards = computed<DashboardCardConfig[]>(() => [
  { id: 'tasks', title: '当前任务', value: String(summary.value.tasks), note: '当前查询结果', x: 0, y: 0, w: 3, h: 2 },
  { id: 'submitted', title: '标注已提交', value: summary.value.submitted.toLocaleString(), note: '用于验收分配输入', x: 3, y: 0, w: 3, h: 2 },
  { id: 'allocated', title: '验收已分配', value: summary.value.allocated.toLocaleString(), note: '实际回查量', x: 6, y: 0, w: 3, h: 2 },
  { id: 'pending', title: '待分配任务', value: String(summary.value.pending), note: '可进入分配预览', x: 9, y: 0, w: 3, h: 2 },
])

async function loadTasks(query = ''): Promise<void> {
  loading.value = true
  error.value = ''
  const spec: QuerySpec = {
    filters: query ? [{ field: 'name', operator: 'contains', value: query }] : [],
    sorting: [{ field: 'expected_delivery_at', direction: 'asc' }],
    page: 1,
    page_size: 20,
  }
  try {
    const response = await queryAcceptanceTasks(spec)
    rows.value = response.items
    computedAt.value = response.computed_at
  } catch {
    error.value = '验收任务读取失败。请确认 FastAPI 与 PostgreSQL 已启动。'
  } finally {
    loading.value = false
  }
}

async function expandTask(row: WorkbenchRow): Promise<void> {
  const task = rows.value.find(item => String(item.id) === String(row.id))
  if (!task || task.children?.length) return
  const children = await getAcceptanceDailyBreakdown(task.id)
  rows.value = rows.value.map(item => item.id === task.id ? { ...item, children } : item)
}

function showPreview(leafIds: string[]): void {
  void generatePreview(leafIds)
}

onMounted(() => loadTasks())
</script>

<template>
  <div class="page-container">
    <header class="page-heading">
      <div><h1>人工质检验收中心</h1><p>任务聚合、按天展开，逐步接入验收分配、通过打回和质量分析</p></div>
      <div class="heading-actions"><select><option>团队验收布局</option><option>我的关注布局</option></select><button @click="editLayout = !editLayout">{{ editLayout ? '完成编辑' : '编辑卡片' }}</button><button>新增卡片</button></div>
    </header>

    <DashboardLayout :cards="summaryCards" :editable="editLayout" @save="editLayout = false" />

    <nav class="work-tabs" aria-label="验收工作区"><button class="active">任务队列</button><button>验收分配</button><button>通过打回</button><button>质量分析</button></nav>

    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <DataWorkbench
      :rows="rows"
      :columns="acceptanceColumns"
      :loading="loading"
      @expand="expandTask"
      @preview="showPreview"
      @selection-change="handleSelectionChange"
      @query-change="loadTasks"
    />

    <AssignmentPreviewPanel
      v-if="previewVisible"
      :preview="preview"
      :loading="previewLoading"
      :error="previewError"
      @close="invalidatePreview"
    />

    <p class="computed-at">数据计算时间：{{ computedAt || '等待后端返回' }}</p>
  </div>
</template>

<style scoped>
.page-container { padding: 28px; }
.page-heading { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 16px; }
.page-heading h1 { margin: 0; font-size: 30px; letter-spacing: -.04em; }
.page-heading p { margin: 4px 0 0; color: var(--color-muted); }
.heading-actions { display: flex; gap: 8px; }
.work-tabs { display: flex; gap: 8px; padding: 12px; border: 1px solid var(--color-line); border-bottom: 0; border-radius: 8px 8px 0 0; background: white; }
.work-tabs .active { color: white; border-color: var(--color-blue); background: var(--color-blue); }
.computed-at { color: var(--color-muted); font-size: 12px; text-align: right; }
.error { padding: 12px; color: #a82936; background: #fbe8ea; }
@media (max-width: 900px) { .page-heading { display: block; } .heading-actions { margin-top: 12px; } }
</style>
