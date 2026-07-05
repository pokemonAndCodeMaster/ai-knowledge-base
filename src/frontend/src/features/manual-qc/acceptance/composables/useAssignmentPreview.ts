import { computed, readonly, shallowRef } from 'vue'

import { createAssignmentPreview } from '../api'
import type { AssignmentPreview, SelectionSpec } from '../types'

export function useAssignmentPreview() {
  const preview = shallowRef<AssignmentPreview | null>(null)
  const loading = shallowRef(false)
  const error = shallowRef('')
  const requested = shallowRef(false)
  const selectionSignature = shallowRef('')

  const visible = computed(() => requested.value || loading.value || preview.value !== null || Boolean(error.value))

  async function generate(explicitIds: string[]): Promise<void> {
    selectionSignature.value = [...explicitIds].sort().join('|')
    requested.value = true
    loading.value = true
    error.value = ''
    preview.value = null
    const selection: SelectionSpec = {
      mode: 'explicit',
      explicit_ids: explicitIds,
      filter_snapshot: null,
      excluded_ids: [],
      leaf_dimension: 'date',
    }
    try {
      preview.value = await createAssignmentPreview(selection)
    } catch {
      error.value = '分配预览生成失败，请检查选择范围或后端服务。'
    } finally {
      loading.value = false
    }
  }

  function invalidate(): void {
    preview.value = null
    error.value = ''
    requested.value = false
    selectionSignature.value = ''
  }

  function handleSelectionChange(explicitIds: string[]): void {
    if (!visible.value) return
    const nextSignature = [...explicitIds].sort().join('|')
    if (nextSignature !== selectionSignature.value) invalidate()
  }

  return {
    preview: readonly(preview),
    loading: readonly(loading),
    error: readonly(error),
    visible,
    generate,
    invalidate,
    handleSelectionChange,
  }
}
