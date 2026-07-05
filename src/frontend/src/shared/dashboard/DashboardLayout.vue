<script setup lang="ts">
import { GridStack, type GridStackWidget } from 'gridstack'
import 'gridstack/dist/gridstack.min.css'
import { nextTick, onBeforeUnmount, onMounted, shallowRef, useTemplateRef, watch } from 'vue'

import type { DashboardCardConfig } from './types'

const props = defineProps<{ cards: DashboardCardConfig[]; editable: boolean }>()
const emit = defineEmits<{ save: [layout: GridStackWidget[]] }>()
const root = useTemplateRef<HTMLElement>('root')
const grid = shallowRef<GridStack | null>(null)

function applyEditable(editable: boolean): void {
  if (!grid.value) return
  grid.value.enableMove(editable)
  grid.value.enableResize(editable)
}

function saveLayout(): void {
  if (!grid.value) return
  emit('save', grid.value.save(false) as GridStackWidget[])
}

onMounted(async () => {
  await nextTick()
  if (!root.value) return
  grid.value = GridStack.init({ column: 12, cellHeight: 72, margin: 8, animate: false, disableDrag: !props.editable, disableResize: !props.editable }, root.value)
})

watch(() => props.editable, applyEditable)
onBeforeUnmount(() => grid.value?.destroy(false))
</script>

<template>
  <section class="dashboard-layout" aria-label="可配置卡片布局">
    <div ref="root" class="grid-stack">
      <article
        v-for="card in cards"
        :key="card.id"
        class="grid-stack-item"
        :gs-id="card.id"
        :gs-x="card.x"
        :gs-y="card.y"
        :gs-w="card.w"
        :gs-h="card.h"
        :gs-no-move="card.locked"
        :gs-no-resize="card.locked"
      >
        <div class="grid-stack-item-content metric-card">
          <span>{{ card.title }}</span><strong>{{ card.value }}</strong><small>{{ card.note }}</small>
          <button v-if="editable" class="card-edit" :aria-label="`编辑${card.title}卡片`">编辑</button>
        </div>
      </article>
    </div>
    <button v-if="editable" class="save-layout" @click="saveLayout">保存当前卡片布局</button>
  </section>
</template>

<style scoped>
.dashboard-layout { margin-bottom: 14px; }
.grid-stack { background: transparent; }
.metric-card { position: relative; display: flex; flex-direction: column; justify-content: center; padding: 16px; border: 1px solid var(--color-line); border-radius: 8px; background: white; }
.metric-card span, .metric-card small { color: var(--color-muted); }
.metric-card strong { margin: 4px 0; font-size: 22px; }
.card-edit { position: absolute; top: 8px; right: 8px; min-height: 28px; font-size: 12px; }
.save-layout { margin-top: 6px; }
</style>
