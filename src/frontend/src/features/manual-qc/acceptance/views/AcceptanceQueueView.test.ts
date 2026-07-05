import { fireEvent, render, screen, waitFor } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { createAssignmentPreview } from '../api'
import AcceptanceQueueView from './AcceptanceQueueView.vue'

vi.mock('../api', () => ({
  queryAcceptanceTasks: vi.fn(async () => ({
    items: [{
      id: 1,
      task_code: 'E2E-001',
      name: '城区测试任务',
      scene_name: 'E2E_CITY',
      topic: '城区',
      priority: 'P0',
      status: 'ACCEPTANCE_RUNNING',
      expected_delivery_at: '2026-07-10',
      expected_quantity: 100,
      annotation_total: 100,
      annotation_submitted: 80,
      annotation_pending: 20,
      acceptance_allocated: 0,
      acceptance_submitted: 0,
      good_allocated: 0,
      good_passed: 0,
      bad_allocated: 0,
      bad_passed: 0,
      recent_annotation_days: [],
    }],
    total: 1,
    page: 1,
    page_size: 20,
    computed_at: '2026-07-05T12:00:00+08:00',
  })),
  getAcceptanceDailyBreakdown: vi.fn(async () => []),
  createAssignmentPreview: vi.fn(async () => ({
    preview_id: 'ap_test123',
    status: 'READY',
    expires_at: '2026-07-05T12:30:00+08:00',
    source_version: 'sha256:test',
    selected_units: 1,
    total_available: 80,
    target_count: 80,
    planned_good: 40,
    planned_bad: 40,
    shortage: 0,
    warnings: [],
    items: [{
      id: '1-date-2026-07-04',
      task_id: 1,
      task_name: '城区测试任务',
      topic: '城区',
      scene_name: 'E2E_CITY',
      stat_date: '2026-07-04',
      available: 80,
      good_available: 40,
      bad_available: 40,
      planned_good: 40,
      planned_bad: 40,
    }],
  })),
}))

describe('AcceptanceQueueView', () => {
  beforeEach(() => vi.clearAllMocks())

  it('验收分配预览只在选择任务并主动点击后出现', async () => {
    render(AcceptanceQueueView, {
      global: { stubs: { DashboardLayout: true } },
    })

    await waitFor(() => expect(screen.getByText('城区测试任务')).toBeTruthy())
    expect(screen.queryByTestId('preview-panel')).toBeNull()

    await fireEvent.click(screen.getByLabelText('选择 城区测试任务'))
    expect(screen.queryByTestId('preview-panel')).toBeNull()

    await fireEvent.click(screen.getByTestId('preview-button'))
    await waitFor(() => expect(createAssignmentPreview).toHaveBeenCalledTimes(1))
    await waitFor(() => expect(screen.getByText(/ap_test123/)).toBeTruthy())
    expect(screen.getAllByText('40 / 40')).toHaveLength(2)

    await fireEvent.click(screen.getByLabelText('选择 城区测试任务'))
    await waitFor(() => expect(screen.queryByTestId('preview-panel')).toBeNull())
  })
})
