import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'

import type { WorkbenchRow } from '@/shared/data-workbench/types'

function numberValue(row: WorkbenchRow, key: string): string {
  return Number(row[key] ?? 0).toLocaleString('zh-CN')
}

export const acceptanceColumns: ColumnDef<WorkbenchRow, unknown>[] = [
  {
    accessorKey: 'name', header: '任务 / 日期', size: 260,
    cell: info => h('div', { class: 'task-cell' }, [h('strong', String(info.row.original.name)), h('small', String(info.row.original.task_code ?? info.row.original.id))]),
  },
  { accessorKey: 'topic', header: '专题', size: 90 },
  { accessorKey: 'priority', header: '优先级', size: 86 },
  { accessorKey: 'status', header: '验收状态', size: 140 },
  { accessorKey: 'expected_delivery_at', header: '交付日期', size: 110 },
  { accessorKey: 'annotation_total', header: '任务总数', size: 110, cell: info => numberValue(info.row.original, 'annotation_total') },
  { accessorKey: 'annotation_submitted', header: '标注已提交', size: 120, cell: info => numberValue(info.row.original, 'annotation_submitted') },
  { accessorKey: 'annotation_pending', header: '标注待完成', size: 120, cell: info => numberValue(info.row.original, 'annotation_pending') },
  {
    id: 'recent_annotation_days', header: '近期新增标注', size: 260, enableSorting: false,
    cell: info => {
      const days = info.row.original.recent_annotation_days as Array<{ stat_date: string; submitted: number }> | undefined
      return days?.length ? days.map(day => `${day.stat_date} +${day.submitted.toLocaleString('zh-CN')}`).join(' · ') : '无新增'
    },
  },
  { accessorKey: 'acceptance_allocated', header: '验收分配', size: 110, cell: info => numberValue(info.row.original, 'acceptance_allocated') },
  { accessorKey: 'acceptance_submitted', header: '验收完成', size: 110, cell: info => numberValue(info.row.original, 'acceptance_submitted') },
  { accessorKey: 'good_allocated', header: 'Good 分配', size: 110, cell: info => numberValue(info.row.original, 'good_allocated') },
  { accessorKey: 'good_passed', header: 'Good 通过', size: 110, cell: info => numberValue(info.row.original, 'good_passed') },
  { accessorKey: 'bad_allocated', header: 'Bad 分配', size: 110, cell: info => numberValue(info.row.original, 'bad_allocated') },
  { accessorKey: 'bad_passed', header: 'Bad 通过', size: 110, cell: info => numberValue(info.row.original, 'bad_passed') },
]
