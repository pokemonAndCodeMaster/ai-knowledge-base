<script setup lang="ts">
import type { AssignmentPreview } from '../types'

defineProps<{
  preview: AssignmentPreview | null
  loading: boolean
  error: string
}>()

defineEmits<{ close: [] }>()
</script>

<template>
  <section class="preview-panel" data-testid="preview-panel" aria-live="polite">
    <header class="preview-header">
      <div>
        <h2 class="preview-title">验收分配预览</h2>
        <p class="preview-subtitle">服务端冻结选择与数据版本；尚未执行真实分配</p>
      </div>
      <button @click="$emit('close')">关闭预览</button>
    </header>

    <p v-if="loading" class="preview-state">正在解析选择并计算 Good/Bad 配额…</p>
    <p v-else-if="error" class="preview-error" role="alert">{{ error }}</p>

    <template v-else-if="preview">
      <div class="preview-metrics">
        <div><span>冻结单元</span><strong>{{ preview.selected_units }}</strong></div>
        <div><span>可用量</span><strong>{{ preview.total_available.toLocaleString() }}</strong></div>
        <div><span>计划 Good</span><strong>{{ preview.planned_good.toLocaleString() }}</strong></div>
        <div><span>计划 Bad</span><strong>{{ preview.planned_bad.toLocaleString() }}</strong></div>
        <div><span>缺口</span><strong>{{ preview.shortage.toLocaleString() }}</strong></div>
      </div>

      <ul v-if="preview.warnings.length" class="preview-warnings">
        <li v-for="warning in preview.warnings" :key="warning">{{ warning }}</li>
      </ul>

      <div class="preview-table-wrap">
        <table class="preview-table">
          <thead><tr><th>任务 / 日期</th><th>可用</th><th>Good 可用 / 计划</th><th>Bad 可用 / 计划</th></tr></thead>
          <tbody>
            <tr v-for="item in preview.items" :key="item.id">
              <td><strong>{{ item.task_name }}</strong><span>{{ item.stat_date }} · {{ item.topic }}</span></td>
              <td>{{ item.available.toLocaleString() }}</td>
              <td>{{ item.good_available.toLocaleString() }} / {{ item.planned_good.toLocaleString() }}</td>
              <td>{{ item.bad_available.toLocaleString() }} / {{ item.planned_bad.toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <footer class="preview-footer">
        <span>Preview：{{ preview.preview_id }}</span>
        <span>有效期至：{{ new Date(preview.expires_at).toLocaleString() }}</span>
        <button class="primary" disabled title="真实 Delta 尚未接入">确认分配（待接 Delta）</button>
      </footer>
    </template>
  </section>
</template>

<style scoped>
.preview-panel { margin-top: 14px; overflow: hidden; border: 1px solid var(--color-line); border-radius: 8px; background: white; }
.preview-header, .preview-footer { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 14px; border-bottom: 1px solid var(--color-line); }
.preview-title, .preview-subtitle { margin: 0; }
.preview-title { font-size: 18px; }
.preview-subtitle, .preview-footer, .preview-table span { color: var(--color-muted); font-size: 12px; }
.preview-state, .preview-error { margin: 0; padding: 24px 14px; }
.preview-error { color: var(--color-danger); }
.preview-metrics { display: grid; grid-template-columns: repeat(5, minmax(110px, 1fr)); border-bottom: 1px solid var(--color-line); }
.preview-metrics div { display: grid; gap: 4px; padding: 14px; border-right: 1px solid var(--color-line-soft); }
.preview-metrics span { color: var(--color-muted); font-size: 12px; }
.preview-metrics strong { font-size: 22px; }
.preview-warnings { margin: 0; padding: 10px 30px; color: var(--color-warning); background: var(--color-warning-soft); }
.preview-table-wrap { overflow-x: auto; }
.preview-table { width: 100%; border-collapse: collapse; }
.preview-table th, .preview-table td { padding: 10px 14px; border-bottom: 1px solid var(--color-line-soft); text-align: left; }
.preview-table td:first-child { display: grid; gap: 2px; }
.preview-footer { border-top: 1px solid var(--color-line); border-bottom: 0; }
.preview-footer span:first-child { font-family: ui-monospace, monospace; }
.primary { color: white; border-color: var(--color-blue); background: var(--color-blue); }
.primary:disabled { cursor: not-allowed; opacity: .55; }
@media (max-width: 760px) { .preview-metrics { grid-template-columns: repeat(2, 1fr); } .preview-footer { align-items: flex-start; flex-direction: column; } }
</style>
