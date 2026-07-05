import {
  FlexRender,
  functionalUpdate,
  getCoreRowModel,
  getExpandedRowModel,
  getSortedRowModel,
  useVueTable,
  type ExpandedState,
  type RowSelectionState,
  type SortingState,
  type VisibilityState,
} from '@tanstack/vue-table'
import { computed, shallowRef, type Ref } from 'vue'

import type { WorkbenchColumn, WorkbenchRow } from './types'

export function useDataWorkbench(rows: Ref<WorkbenchRow[]>, columns: Ref<WorkbenchColumn[]>) {
  const rowSelection = shallowRef<RowSelectionState>({})
  const expanded = shallowRef<ExpandedState>({})
  const sorting = shallowRef<SortingState>([])
  const columnVisibility = shallowRef<VisibilityState>({})

  const table = useVueTable({
    get data() { return rows.value },
    get columns() { return columns.value },
    getRowId: row => String(row.id),
    getSubRows: row => row.children,
    enableRowSelection: true,
    enableSubRowSelection: true,
    columnResizeMode: 'onChange',
    state: {
      get rowSelection() { return rowSelection.value },
      get expanded() { return expanded.value },
      get sorting() { return sorting.value },
      get columnVisibility() { return columnVisibility.value },
    },
    onRowSelectionChange: updater => { rowSelection.value = functionalUpdate(updater, rowSelection.value) },
    onExpandedChange: updater => { expanded.value = functionalUpdate(updater, expanded.value) },
    onSortingChange: updater => { sorting.value = functionalUpdate(updater, sorting.value) },
    onColumnVisibilityChange: updater => { columnVisibility.value = functionalUpdate(updater, columnVisibility.value) },
    getCoreRowModel: getCoreRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    getSortedRowModel: getSortedRowModel(),
  })

  const selectedLeafIds = computed(() => table.getSelectedRowModel().flatRows.filter(row => !row.subRows.length).map(row => row.id))

  return { table, rowSelection, expanded, sorting, columnVisibility, selectedLeafIds, FlexRender }
}
