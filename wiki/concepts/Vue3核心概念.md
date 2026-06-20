---
title: Vue3 核心概念
domain: ["meta"]
type: "concept"
tags: [Vue3, 前端框架, 响应式, Composition API, 组件]
created: 2026-06-19
updated: 2026-06-19
sources: 2
status: active
related_code: ["src/frontend/"]
affects_path: []
trigger_keywords: [Vue3, 响应式, ref, reactive, computed, watch, 组件通信, 生命周期, Composition API]
---

# 🟢 Vue 3 核心概念

> **定位**：深度理解 Vue 3 的核心机制。[[前端从零到精通学习指南]] 中的 P0-P2 阶段会引用本卡片。
> **关联**：[[前端开发规范]] | [[数据质量门户架构设计]]

---

## 1. 响应式系统 — Vue 的灵魂

### 1.1 什么是响应式

**核心思想**：你只管修改数据，Vue 自动帮你更新页面。

```
传统方式：
  数据变了 → 你手动找到 DOM 元素 → 你手动改它的内容
  
Vue 方式：
  数据变了 → Vue 自动检测到变化 → 自动更新所有引用了这个数据的地方
```

### 1.2 底层原理：Proxy 代理

Vue 3 使用 JavaScript 的 `Proxy` 对象来实现响应式。`Proxy` 可以拦截对象的读取和修改操作。

```javascript
// 简化的原理演示（Vue 内部的大致逻辑）
const data = { count: 0 }

const proxy = new Proxy(data, {
  get(target, key) {
    track(target, key)    // ★ 读取时：记录"谁在用这个数据"
    return target[key]
  },
  set(target, key, value) {
    target[key] = value
    trigger(target, key)  // ★ 修改时：通知所有用到这个数据的地方更新
    return true
  },
})

proxy.count = 42  // 触发 set → trigger → 页面自动更新
```

### 1.3 ref vs reactive

```typescript
import { ref, reactive } from 'vue'

// ── ref：用于基本类型（string, number, boolean）和对象 ──
const count = ref(0)         // 包装成 { value: 0 }
count.value++                // script 中通过 .value 访问
// template 中自动解包：{{ count }} 直接用，不需要 .value

// ── reactive：用于对象/数组（不需要 .value） ──
const form = reactive({
  name: '',
  status: 'pending',
})
form.name = '新任务'          // 直接赋值，不需要 .value

// ★ 推荐策略：统一使用 ref，不用纠结选哪个
// 理由：
//   1. ref 可以存任何类型（基本类型和对象都行）
//   2. 始终用 .value 访问，心智模型统一
//   3. 解构赋值时不会丢失响应性（reactive 会！）
```

**reactive 的陷阱**（这就是为什么推荐 ref）：

```typescript
const state = reactive({ name: '张三', age: 25 })

// ❌ 解构后丢失响应式！
const { name, age } = state    // name 和 age 变成普通变量了
name = '李四'                   // 不会触发页面更新

// ✅ 用 ref 就没有这个问题
const name = ref('张三')
const nameAlias = name          // 仍然是响应式的
```

### 1.4 computed — 计算属性

```typescript
import { ref, computed } from 'vue'

const tasks = ref([
  { id: 1, status: 'done' },
  { id: 2, status: 'pending' },
  { id: 3, status: 'done' },
])

// computed 会缓存结果
// 只有 tasks 变化时才重新计算
const doneCount = computed(() =>
  tasks.value.filter(t => t.status === 'done').length
)

// ★ 和直接写函数的区别：
// function getDoneCount() { return tasks.value.filter(...).length }
// 函数每次调用都会重新计算
// computed 只有依赖变了才重新计算（性能更好）
```

### 1.5 watch — 侦听器

```typescript
import { ref, watch } from 'vue'

const searchText = ref('')

// 当 searchText 变化时，执行回调
watch(searchText, (newVal, oldVal) => {
  console.log(`搜索词从 "${oldVal}" 变为 "${newVal}"`)
  // 可以在这里发起搜索请求
})

// 侦听多个数据
watch([page, status], ([newPage, newStatus]) => {
  loadData()  // 页码或状态变了就重新加载
})

// 立即执行一次
watch(searchText, (val) => {
  search(val)
}, { immediate: true })  // 组件创建时也执行一次
```

**computed vs watch 选择策略**：

```
需要根据数据 A 计算出数据 B → 用 computed
  例：根据任务列表计算"已完成数量"

需要在数据变化时执行副作用（发请求、写日志等）→ 用 watch
  例：搜索框内容变化时发起搜索请求
```

---

## 2. Composition API — Vue 3 的编程方式

### 2.1 和 Options API 的对比

Vue 2 使用 Options API（按选项分类），Vue 3 推荐 Composition API（按功能分组）：

```vue
<!-- ❌ Options API（Vue 2 风格，不推荐新代码使用） -->
<script>
export default {
  data() {
    return { count: 0, name: '' }  // 数据散落在 data 中
  },
  computed: {
    doubled() { return this.count * 2 }  // 计算属性在 computed 中
  },
  methods: {
    increment() { this.count++ }  // 方法在 methods 中
  },
  mounted() {
    this.loadData()  // 生命周期在各自的钩子中
  },
}
// 问题：同一个功能的代码（数据、计算、方法）被拆散到不同地方
</script>

<!-- ✅ Composition API（Vue 3 风格，推荐） -->
<script setup lang="ts">
// 同一个功能的代码放在一起
const count = ref(0)
const doubled = computed(() => count.value * 2)
function increment() { count.value++ }

// 另一个功能的代码也放在一起
const name = ref('')
function updateName(val: string) { name.value = val }

onMounted(() => loadData())
</script>
```

### 2.2 `<script setup>` 语法糖

`<script setup>` 是 Composition API 的简写形式，它做了以下事情：

```vue
<!-- 使用 <script setup>（推荐） -->
<script setup lang="ts">
const count = ref(0)        // 自动暴露给模板，不需要 return
function increment() { ... } // 自动暴露给模板
</script>

<!-- 等价的完整写法（了解即可，不需要这样写） -->
<script lang="ts">
import { defineComponent, ref } from 'vue'
export default defineComponent({
  setup() {
    const count = ref(0)
    function increment() { ... }
    return { count, increment }  // 需要手动 return
  },
})
</script>
```

---

## 3. 组件通信模式

### 3.1 模式总览

```
父 → 子：props（传数据下去）
子 → 父：emit（发事件上去）
兄弟/跨层级：Pinia Store（共享状态）
祖先 → 后代：provide/inject（跨多层传递）
```

### 3.2 Props 详解

```typescript
// 方式一：纯类型定义（推荐，TypeScript 友好）
const props = defineProps<{
  taskId: number                              // 必填
  title: string                               // 必填
  status?: 'pending' | 'running' | 'done'     // 可选
  readonly?: boolean                          // 可选
}>()

// 方式二：带默认值
const props = withDefaults(
  defineProps<{
    title: string
    size?: 'small' | 'medium' | 'large'
  }>(),
  {
    size: 'medium',  // 默认值
  }
)
```

**Props 是只读的**：

```typescript
// ❌ 不能修改 props！
props.title = '新标题'  // TypeScript 会报错

// ✅ 如果需要基于 props 的派生数据，用 computed
const displayTitle = computed(() => `[${props.status}] ${props.title}`)
```

### 3.3 Emits 详解

```typescript
// 定义事件（带类型）
const emit = defineEmits<{
  'update': [task: LlmQcTask]           // 事件名: [参数类型]
  'delete': [taskId: number]
  'status-change': [id: number, status: string]
}>()

// 触发事件
emit('delete', task.id)
emit('status-change', task.id, 'completed')
```

### 3.4 provide/inject（跨多层传递）

```typescript
// 祖先组件提供数据
import { provide } from 'vue'
const theme = ref('dark')
provide('theme', theme)

// 任意后代组件注入数据（不管嵌套多深）
import { inject } from 'vue'
const theme = inject<Ref<string>>('theme', ref('light'))  // 第二个参数是默认值
```

---

## 4. 生命周期

```
组件创建 → setup()（<script setup> 中的代码直接执行）
     ↓
模板编译 → 不需要你管
     ↓
挂载到页面 → onMounted()  ★ 最常用：在这里发请求加载数据
     ↓
数据更新导致重渲染 → onUpdated()  很少用
     ↓
组件从页面移除 → onUnmounted()  ★ 常用：清理定时器、取消事件监听
```

```typescript
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  // 组件已经显示在页面上了
  loadData()                // 发请求加载数据
  window.addEventListener('resize', handleResize)  // 监听窗口大小
})

onUnmounted(() => {
  // 组件要被销毁了
  window.removeEventListener('resize', handleResize)  // 清理监听
})
```

---

## 5. 模板中的高级用法

### 5.1 插槽 Slot（组件的"占位符"）

```vue
<!-- 通用卡片组件 Card.vue -->
<template>
  <div class="card">
    <div class="card-header">
      <slot name="header">默认标题</slot>   <!-- 具名插槽 -->
    </div>
    <div class="card-body">
      <slot></slot>                          <!-- 默认插槽 -->
    </div>
    <div class="card-footer">
      <slot name="footer"></slot>            <!-- 具名插槽 -->
    </div>
  </div>
</template>

<!-- 使用时 -->
<Card>
  <template #header>
    <h3>任务详情</h3>
  </template>
  
  <!-- 默认插槽内容 -->
  <p>任务描述...</p>
  
  <template #footer>
    <el-button>提交</el-button>
  </template>
</Card>
```

### 5.2 动态组件

```vue
<template>
  <!-- 根据 currentTab 动态切换显示的组件 -->
  <component :is="tabComponents[currentTab]" />
</template>

<script setup>
const currentTab = ref('overview')
const tabComponents = {
  overview: OverviewPanel,
  detail: DetailPanel,
  chart: ChartPanel,
}
</script>
```

---

> ⚠️ 关联经验与规范：[[前端开发规范]]
> ✅ 支持：[[前端从零到精通学习指南]]
