import { fireEvent, render, screen } from '@testing-library/vue'
import type { ColumnDef } from '@tanstack/vue-table'
import { describe, expect, it } from 'vitest'

import DataWorkbench from './DataWorkbench.vue'
import type { WorkbenchRow } from './types'

const columns: ColumnDef<WorkbenchRow, unknown>[] = [
  { accessorKey: 'name', header: '任务' },
  { accessorKey: 'value', header: '数量' },
]

const rows: WorkbenchRow[] = [
  {
    id: 'parent',
    name: '任务A',
    value: 30,
    children: [
      { id: 'day-1', name: '07-04 日明细', value: 10 },
      { id: 'day-2', name: '07-03 日明细', value: 20 },
    ],
  },
]

describe('DataWorkbench', () => {
  it('默认隐藏分析配置，点击后才显示', async () => {
    render(DataWorkbench, { props: { rows, columns } })
    expect(screen.queryByTestId('analysis-panel')).toBeNull()
    await fireEvent.click(screen.getByRole('button', { name: '一键统计分析' }))
    expect(screen.getByTestId('analysis-panel')).toBeTruthy()
  })

  it('勾选聚合行会选中全部叶子行', async () => {
    render(DataWorkbench, { props: { rows, columns } })
    expect(screen.queryByTestId('preview-button')).toBeNull()
    await fireEvent.click(screen.getByLabelText('选择 任务A'))
    expect(screen.getByText('已选 2 个最小单元')).toBeTruthy()
    expect(screen.getByTestId('preview-button')).toBeTruthy()
  })

  it('展开后子行保持被选中，取消子行后父行进入半选', async () => {
    render(DataWorkbench, { props: { rows, columns } })
    await fireEvent.click(screen.getByLabelText('选择 任务A'))
    await fireEvent.click(screen.getByRole('button', { name: '+' }))
    const child = screen.getByLabelText('选择 07-04 日明细') as HTMLInputElement
    expect(child.checked).toBe(true)
    await fireEvent.click(child)
    const parent = screen.getByLabelText('选择 任务A') as HTMLInputElement
    expect(parent.indeterminate).toBe(true)
  })
})
