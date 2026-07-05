import { nextTick } from 'vue'
import { describe, expect, it, vi } from 'vitest'

import { createAssignmentPreview } from '../api'
import { useAssignmentPreview } from './useAssignmentPreview'

vi.mock('../api', () => ({
  createAssignmentPreview: vi.fn(async () => ({
    preview_id: 'ap_composable',
    status: 'READY',
    expires_at: '2026-07-06T08:30:00+08:00',
    source_version: 'sha256:test',
    selected_units: 1,
    total_available: 10,
    target_count: 10,
    planned_good: 5,
    planned_bad: 5,
    shortage: 0,
    items: [],
    warnings: [],
  })),
}))

describe('useAssignmentPreview', () => {
  it('生成后保持可见，只有选择变化才失效', async () => {
    const state = useAssignmentPreview()
    await state.generate(['1'])
    expect(createAssignmentPreview).toHaveBeenCalledOnce()
    expect(state.visible.value).toBe(true)
    expect(state.preview.value?.preview_id).toBe('ap_composable')

    state.handleSelectionChange(['1'])
    await nextTick()
    expect(state.visible.value).toBe(true)

    state.handleSelectionChange(['2'])
    await nextTick()
    expect(state.visible.value).toBe(false)
  })
})
