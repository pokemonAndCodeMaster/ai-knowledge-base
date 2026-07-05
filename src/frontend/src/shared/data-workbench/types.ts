import type { ColumnDef } from '@tanstack/vue-table'

export interface WorkbenchRow {
  id: string | number
  children?: WorkbenchRow[]
  [key: string]: unknown
}

export type WorkbenchColumn = ColumnDef<WorkbenchRow, unknown>
