import { http } from '@/shared/api/http'
import type { ApiResponse } from '@/shared/api/types'

import type { AcceptanceDay, AcceptanceTaskPage, AssignmentPreview, QuerySpec, SelectionSpec } from './types'

export async function queryAcceptanceTasks(spec: QuerySpec): Promise<AcceptanceTaskPage> {
  const response = await http.post<ApiResponse<AcceptanceTaskPage>>('/manual-qc/acceptance/tasks/query', spec)
  return response.data.data
}

export async function getAcceptanceDailyBreakdown(taskId: number): Promise<AcceptanceDay[]> {
  const response = await http.get<ApiResponse<Array<{
    id: string
    stat_date: string
    annotation_total: number
    annotation_submitted: number
    annotation_pending: number
    acceptance_allocated: number
    acceptance_submitted: number
    good_allocated: number
    good_passed: number
    bad_allocated: number
    bad_passed: number
  }>>>(
    `/manual-qc/acceptance/tasks/${taskId}/breakdown`,
    { params: { dimension: 'date' } },
  )
  return response.data.data.map(item => ({
    ...item,
    name: `${item.stat_date} 日明细`,
    topic: '',
    priority: '',
    status: 'DATE_DETAIL',
    expected_delivery_at: null,
    recent_annotation_days: [],
  }))
}

export async function createAssignmentPreview(selection: SelectionSpec): Promise<AssignmentPreview> {
  const response = await http.post<ApiResponse<AssignmentPreview>>('/manual-qc/acceptance/assignment/preview', {
    selection,
    rule: { strategy: 'ratio', good_ratio: 0.5 },
  })
  return response.data.data
}
