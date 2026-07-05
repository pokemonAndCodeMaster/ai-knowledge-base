<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, shallowRef, toRef, useTemplateRef } from 'vue'

import IndeterminateCheckbox from './IndeterminateCheckbox.vue'
import type { WorkbenchColumn, WorkbenchRow } from './types'
import { useDataWorkbench } from './useDataWorkbench'

const props = withDefaults(defineProps<{
  rows: WorkbenchRow[]
  columns: WorkbenchColumn[]
  loading?: boolean
}>(), { loading: false })

const emit = defineEmits<{
  expand: [row: WorkbenchRow]
  preview: [leafIds: string[]]
  selectionChange: [leafIds: string[]]
  queryChange: [query: string]
}>()

const rowsRef = toRef(props, 'rows')
const columnsRef = toRef(props, 'columns')
const { table, selectedLeafIds, FlexRender } = useDataWorkbench(rowsRef, columnsRef)
const showColumns = shallowRef(false)
const showAnalysis = shallowRef(false)
const query = shallowRef('')
const root = useTemplateRef<HTMLElement>('root')
const viewport = useTemplateRef<HTMLElement>('viewport')
const proxy = useTemplateRef<HTMLElement>('proxy')
const showProxy = shallowRef(false)
const proxyStyle = shallowRef<Record<string, string>>({})
const proxyWidth = shallowRef(0)

const selectedCount = computed(() => selectedLeafIds.value.length)

function toggleRow(row: ReturnType<typeof table.getRowModel>['rows'][number]): void {
  row.toggleExpanded()
  if (row.getIsExpanded()) emit('expand', row.original)
}

function requestPreview(): void {
  if (selectedLeafIds.value.length) emit('preview', selectedLeafIds.value)
}

async function toggleRowSelection(row: ReturnType<typeof table.getRowModel>['rows'][number], checked: boolean): Promise<void> {
  row.toggleSelected(checked)
  await nextTick()
  if (row.depth > 0) {
    const parent = table.getRow(row.parentId as string)
    const allChildrenSelected = parent.subRows.every(child => child.getIsSelected())
    parent.toggleSelected(allChildrenSelected, { selectChildren: false })
    await nextTick()
  }
  emit('selectionChange', selectedLeafIds.value)
}

async function toggleAllRows(checked: boolean): Promise<void> {
  table.toggleAllRowsSelected(checked)
  await nextTick()
  emit('selectionChange', selectedLeafIds.value)
}

function clearSelection(): void {
  table.resetRowSelection()
  emit('selectionChange', [])
}

function isRowChecked(row: ReturnType<typeof table.getRowModel>['rows'][number]): boolean {
  return row.subRows.length ? row.subRows.every(child => child.getIsSelected()) : row.getIsSelected()
}

function isRowIndeterminate(row: ReturnType<typeof table.getRowModel>['rows'][number]): boolean {
  if (!row.subRows.length) return false
  const selectedChildren = row.subRows.filter(child => child.getIsSelected()).length
  return selectedChildren > 0 && selectedChildren < row.subRows.length
}

function updateProxy(): void {
  const rootElement = root.value
  const viewportElement = viewport.value
  if (!rootElement || !viewportElement) return
  const rect = rootElement.getBoundingClientRect()
  showProxy.value = viewportElement.scrollWidth > viewportElement.clientWidth && rect.top < window.innerHeight && rect.bottom > window.innerHeight
  proxyWidth.value = viewportElement.scrollWidth
  proxyStyle.value = { left: `${viewportElement.getBoundingClientRect().left}px`, width: `${viewportElement.clientWidth}px` }
}

function syncFromProxy(): void {
  if (viewport.value && proxy.value) viewport.value.scrollLeft = proxy.value.scrollLeft
}

function syncFromViewport(): void {
  if (viewport.value && proxy.value) proxy.value.scrollLeft = viewport.value.scrollLeft
}

onMounted(async () => {
  await nextTick()
  updateProxy()
  window.addEventListener('scroll', updateProxy, { passive: true })
  window.addEventListener('resize', updateProxy)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', updateProxy)
  window.removeEventListener('resize', updateProxy)
})
</script>

<template>
  <section ref="root" class="workbench" aria-label="统一数据工作台">
    <div class="workbench-toolbar">
      <select aria-label="布局配置"><option>团队默认布局</option><option>我的关注任务</option></select>
      <button @click="showColumns = !showColumns">列显示与布局</button>
      <button @click="showAnalysis = !showAnalysis">一键统计分析</button>
      <button>导出 Excel</button>
      <input v-model="query" placeholder="搜索当前任务" aria-label="搜索当前任务" @change="emit('queryChange', query)">
    </div>

    <div v-if="showColumns" class="column-panel" data-testid="column-panel">
      <label v-for="column in table.getAllLeafColumns()" :key="column.id">
        <input type="checkbox" :checked="column.getIsVisible()" @change="column.toggleVisibility()">
        {{ column.columnDef.header }}
      </label>
      <button>另存为个人布局</button>
    </div>

    <div v-if="showAnalysis" class="analysis-panel" data-testid="analysis-panel">
      <label>分析维度<select><option>专题</option><option>任务</option><option>日期</option></select></label>
      <label>分析指标<select><option>标注提交量</option><option>验收通过率</option></select></label>
      <label>图表形式<select><option>趋势图</option><option>分组柱图</option></select></label>
      <button class="primary">生成图表并加入布局</button>
    </div>

    <div v-if="selectedCount" class="batch-bar">
      <strong>已选 {{ selectedCount }} 个最小单元</strong>
      <button class="primary" data-testid="preview-button" @click="requestPreview">生成分配预览</button>
      <button>加入关注</button>
      <button @click="clearSelection">取消选择</button>
    </div>

    <div ref="viewport" class="table-viewport" @scroll="syncFromViewport">
      <table :style="{ width: `${table.getTotalSize()}px` }">
        <thead>
          <tr v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
            <th class="selection-cell">
              <IndeterminateCheckbox
                :checked="table.getIsAllRowsSelected()"
                :indeterminate="table.getIsSomeRowsSelected()"
                label="全选当前已加载任务及子行"
                @change="toggleAllRows"
              />
            </th>
            <th v-for="header in headerGroup.headers" :key="header.id" :style="{ width: `${header.getSize()}px` }">
              <button class="header-button" :disabled="!header.column.getCanSort()" @click="header.column.getToggleSortingHandler()?.($event)">
                <FlexRender :render="header.column.columnDef.header" :props="header.getContext()" />
                <span v-if="header.column.getIsSorted()">{{ header.column.getIsSorted() === 'asc' ? '↑' : '↓' }}</span>
              </button>
              <span class="resize-handle" @mousedown="header.getResizeHandler()($event)" @touchstart="header.getResizeHandler()($event)" />
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td :colspan="table.getVisibleLeafColumns().length + 1" class="empty">正在读取验收任务…</td></tr>
          <tr v-for="row in table.getRowModel().rows" v-else :key="row.id" :class="{ 'child-row': row.depth > 0 }">
            <td class="selection-cell">
              <IndeterminateCheckbox
                :checked="isRowChecked(row)"
                :indeterminate="isRowIndeterminate(row)"
                :label="`选择 ${String(row.original.name ?? row.id)}`"
                @change="toggleRowSelection(row, $event)"
              />
            </td>
            <td v-for="(cell, index) in row.getVisibleCells()" :key="cell.id" :style="{ width: `${cell.column.getSize()}px` }">
              <button v-if="index === 0 && row.getCanExpand()" class="expand-button" :aria-expanded="row.getIsExpanded()" @click="toggleRow(row)">
                {{ row.getIsExpanded() ? '−' : '+' }}
              </button>
              <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
            </td>
          </tr>
          <tr v-if="!loading && !table.getRowModel().rows.length"><td :colspan="table.getVisibleLeafColumns().length + 1" class="empty">当前筛选下没有任务</td></tr>
        </tbody>
      </table>
    </div>

    <div v-show="showProxy" ref="proxy" class="viewport-scrollbar" :style="proxyStyle" @scroll="syncFromProxy">
      <div :style="{ width: `${proxyWidth}px`, height: '1px' }" />
    </div>
  </section>
</template>

<style scoped>
.workbench { overflow: hidden; border: 1px solid var(--color-line); border-radius: 8px; background: white; }
.workbench-toolbar, .batch-bar { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; padding: 10px 12px; border-bottom: 1px solid var(--color-line); }
.workbench-toolbar input { margin-left: auto; }
.column-panel, .analysis-panel { display: grid; grid-template-columns: repeat(4, minmax(150px, 1fr)); gap: 8px; padding: 12px; border-bottom: 1px solid var(--color-line); background: #f8fafc; }
.column-panel label { display: flex; align-items: center; gap: 6px; }
.analysis-panel label { display: grid; gap: 4px; color: var(--color-muted); font-size: 12px; }
.batch-bar { position: sticky; top: 64px; z-index: 5; color: #183d94; background: var(--color-blue-soft); }
.table-viewport { overflow: auto; scrollbar-width: none; }
.table-viewport::-webkit-scrollbar { height: 0; }
table { min-width: 1100px; border-collapse: collapse; table-layout: fixed; }
th, td { height: 48px; padding: 8px 10px; border-bottom: 1px solid var(--color-line-soft); overflow: hidden; text-align: left; text-overflow: ellipsis; white-space: nowrap; }
th { position: relative; color: var(--color-muted); background: #f1f4f7; font-size: 12px; }
.header-button { border: 0; padding: 0; background: transparent; font-weight: 750; }
.resize-handle { position: absolute; inset: 0 -2px 0 auto; width: 5px; cursor: col-resize; }
.selection-cell { position: sticky; left: 0; z-index: 3; width: 42px; background: white; }
th.selection-cell { background: #f1f4f7; }
.child-row td { background: #f8fafc; }
.child-row td:nth-child(2) { padding-left: 30px; }
.expand-button { width: 24px; border: 0; background: transparent; font-weight: 800; }
.viewport-scrollbar { position: fixed; z-index: 20; bottom: 0; height: 16px; overflow-x: auto; overflow-y: hidden; border: 1px solid var(--color-line); background: #edf1f5; }
.empty { height: 150px; color: var(--color-muted); text-align: center; }
.primary { color: white; border-color: var(--color-blue); background: var(--color-blue); }
@media (max-width: 760px) { .column-panel, .analysis-panel { grid-template-columns: 1fr; } .workbench-toolbar input { margin-left: 0; } }
</style>
