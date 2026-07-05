<script setup lang="ts">
import { onMounted, useTemplateRef, watch } from 'vue'

const props = defineProps<{ checked: boolean; indeterminate?: boolean; label: string }>()
const emit = defineEmits<{ change: [checked: boolean] }>()
const input = useTemplateRef<HTMLInputElement>('input')

function syncIndeterminate(): void {
  if (input.value) input.value.indeterminate = Boolean(props.indeterminate && !props.checked)
}

onMounted(syncIndeterminate)
watch(() => props.indeterminate, syncIndeterminate)
watch(() => props.checked, syncIndeterminate)
</script>

<template>
  <input
    ref="input"
    type="checkbox"
    :checked="checked"
    :aria-label="label"
    @change="emit('change', ($event.target as HTMLInputElement).checked)"
  >
</template>
