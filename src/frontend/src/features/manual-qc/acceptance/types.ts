import type { WorkbenchRow } from '@/shared/data-workbench/types'

export interface RecentAnnotationDay {
  stat_date: string
  submitted: number
}

export interface AcceptanceTask extends WorkbenchRow {
  id: number
  task_code: string
  name: string
  scene_name: string
  topic: string
  priority: string
  status: string
  expected_delivery_at: string | null
  expected_quantity: number
  annotation_total: number
  annotation_submitted: number
  annotation_pending: number
  acceptance_allocated: number
  acceptance_submitted: number
  good_allocated: number
  good_passed: number
  bad_allocated: number
  bad_passed: number
  recent_annotation_days: RecentAnnotationDay[]
  children?: AcceptanceDay[]
}

export interface AcceptanceDay extends WorkbenchRow {
  id: string
  name: string
  stat_date: string
  topic: string
  priority: string
  status: string
  expected_delivery_at: string | null
  annotation_total: number
  annotation_submitted: number
  annotation_pending: number
  acceptance_allocated: number
  acceptance_submitted: number
  good_allocated: number
  good_passed: number
  bad_allocated: number
  bad_passed: number
  recent_annotation_days: RecentAnnotationDay[]
}

export interface AcceptanceTaskPage {
  items: AcceptanceTask[]
  total: number
  page: number
  page_size: number
  computed_at: string
}

export interface QuerySpec {
  filters: Array<{ field: string; operator: 'contains' | 'eq' | 'in'; value: unknown }>
  sorting: Array<{ field: string; direction: 'asc' | 'desc' }>
  page: number
  page_size: number
}

export interface SelectionSpec {
  mode: 'explicit' | 'filtered'
  explicit_ids: string[]
  filter_snapshot: QuerySpec | null
  excluded_ids: string[]
  leaf_dimension: 'task' | 'date' | 'group' | 'annotator' | 'scene'
}

export interface AssignmentPreviewItem {
  id: string
  task_id: number
  task_name: string
  topic: string
  scene_name: string
  stat_date: string
  available: number
  good_available: number
  bad_available: number
  planned_good: number
  planned_bad: number
}

export interface AssignmentPreview {
  preview_id: string
  status: 'READY'
  expires_at: string
  source_version: string
  selected_units: number
  total_available: number
  target_count: number
  planned_good: number
  planned_bad: number
  shortage: number
  items: readonly AssignmentPreviewItem[]
  warnings: readonly string[]
}
