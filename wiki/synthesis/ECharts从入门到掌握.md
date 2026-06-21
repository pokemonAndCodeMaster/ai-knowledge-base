---
title: ECharts从入门到掌握
domain: ["tooling", "ai_dlc"]
type: "synthesis"
tags: [前端, ECharts, 可视化, Vue3, 图表, 质检平台]
created: 2026-06-21
updated: 2026-06-21
sources: 3
status: active
related_code: ["src/frontend/"]
affects_path: ["src/frontend/"]
trigger_keywords: [ECharts, 图表, 可视化, 折线图, 柱状图, 饼图, Vue3图表, chart option]
---

# ECharts从入门到掌握

本卡回答：ECharts 是什么、怎么安装、代码放哪里、每一步输入输出是什么、如何和后端/页面/组件联动。

## 1. ECharts 是什么

ECharts 是浏览器里的图表渲染库。你给它一个 DOM 容器和一份 `option` 配置，它把配置渲染成折线图、柱状图、饼图、仪表盘、热力图等。

最小心智模型：

```text
后端数据 JSON -> 前端转换函数 -> ECharts option -> echarts.setOption(option) -> 浏览器图表
```

ECharts 不负责查数据库，不负责调后端，也不负责页面布局。它只负责把前端给它的数据画出来。

## 2. 安装

在前端工程目录安装：

```bash
cd src/frontend
pnpm add echarts
```

如果还没初始化前端工程，先用：

```bash
cd src
pnpm create vite frontend --template vue-ts
cd frontend
pnpm add vue-router@4 pinia axios element-plus @element-plus/icons-vue echarts
```

## 3. 代码应该放哪里

推荐目录：

```text
src/frontend/src/
├── shared/
│   ├── charts/
│   │   ├── BaseChart.vue          # 通用图表容器
│   │   ├── chartTheme.ts          # 全站图表主题
│   │   └── chartOptions.ts        # 通用 option 构造函数
│   └── utils/
│       └── format.ts              # 数字、百分比、日期格式化
└── features/
    └── llm-qc/
        ├── api.ts                 # 调后端拿图表数据
        ├── types.ts               # 图表数据类型
        ├── views/
        │   └── TaskDashboard.vue  # 页面容器
        └── components/
            └── TaskStatusChart.vue # 本模块图表组件
```

放置原则：

- `BaseChart.vue`：所有模块都能用的通用图表壳。
- `chartOptions.ts`：通用折线图、柱状图、饼图 option 构造函数。
- `features/<module>/components/*Chart.vue`：有业务语义的图表，如任务状态分布、通道耗时趋势。
- `features/<module>/api.ts`：从后端拿数据。
- `features/<module>/types.ts`：定义后端返回的数据结构。

## 4. 最小代码：BaseChart

`BaseChart.vue` 只关心三件事：拿到 `option`、初始化 echarts、窗口变化时 resize。

```vue
<template>
  <div ref="chartRef" class="base-chart" />
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

const props = defineProps<{
  option: EChartsOption
}>()

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null

function renderChart() {
  if (!chartRef.value) return
  if (!chart) {
    chart = echarts.init(chartRef.value)
  }
  chart.setOption(props.option, true)
}

function resizeChart() {
  chart?.resize()
}

watch(() => props.option, renderChart, { deep: true })

onMounted(() => {
  renderChart()
  window.addEventListener('resize', resizeChart)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeChart)
  chart?.dispose()
  chart = null
})
</script>

<style scoped>
.base-chart {
  width: 100%;
  height: 320px;
}
</style>
```

输入：`option`。

输出：浏览器中的图表。

生命周期：组件挂载时初始化，`option` 变化时重绘，组件销毁时释放图表实例。

## 5. 后端返回什么数据

不要让后端直接返回 ECharts option。后端应该返回业务数据，前端负责转成图表配置。

推荐后端响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {"status": "pending", "count": 12},
      {"status": "running", "count": 3},
      {"status": "failed", "count": 2},
      {"status": "completed", "count": 40}
    ]
  }
}
```

前端类型：

```ts
export interface TaskStatusCount {
  status: string
  count: number
}

export interface TaskStatusSummary {
  items: TaskStatusCount[]
}
```

## 6. 前端如何转 option

```ts
import type { EChartsOption } from 'echarts'
import type { TaskStatusCount } from './types'

export function buildTaskStatusPieOption(items: TaskStatusCount[]): EChartsOption {
  return {
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [
      {
        name: '任务状态',
        type: 'pie',
        radius: ['45%', '70%'],
        data: items.map(item => ({
          name: item.status,
          value: item.count,
        })),
      },
    ],
  }
}
```

输入：业务数组 `TaskStatusCount[]`。

输出：ECharts 认识的 `EChartsOption`。

好处：后端稳定表达业务事实，前端可以独立调整图表样式。

## 7. 业务图表组件怎么写

```vue
<template>
  <BaseChart :option="chartOption" />
</template>

<script setup lang="ts">
import { computed } from 'vue'

import BaseChart from '@/shared/charts/BaseChart.vue'
import type { TaskStatusCount } from '../types'
import { buildTaskStatusPieOption } from '../chartOptions'

const props = defineProps<{
  items: TaskStatusCount[]
}>()

const chartOption = computed(() => buildTaskStatusPieOption(props.items))
</script>
```

这个组件不调 API，只接收数据并画图。这样它可以被 Dashboard、详情页、弹窗复用。

## 8. 页面怎么用图表

```vue
<template>
  <section>
    <TaskStatusChart :items="summary.items" />
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

import { getTaskStatusSummary } from '../api'
import TaskStatusChart from '../components/TaskStatusChart.vue'
import type { TaskStatusSummary } from '../types'

const summary = ref<TaskStatusSummary>({ items: [] })

async function loadSummary() {
  summary.value = await getTaskStatusSummary()
}

onMounted(loadSummary)
</script>
```

完整链路：

```text
TaskDashboard.vue -> getTaskStatusSummary() -> FastAPI -> Application Service -> Repository -> PostgreSQL
TaskDashboard.vue -> TaskStatusChart -> BaseChart -> ECharts
```

## 9. 常见图表对应关系

| 需求 | 推荐图表 | 后端返回 |
|---|---|---|
| 任务状态占比 | 饼图/环形图 | `[{status,count}]` |
| 每日任务量趋势 | 折线图 | `[{date,count}]` |
| 各通道耗时对比 | 柱状图 | `[{channel,avg_seconds}]` |
| 错误类型分布 | 横向柱状图 | `[{error_type,count}]` |
| Pipeline 阶段耗时 | 堆叠柱状图 / 甘特风格 | `[{task_id,stage,start,end}]` |
| 成功率/失败率 | 折线图 + 百分比 | `[{date,success_rate}]` |

## 10. 可维护规则

- 后端返回业务数据，不返回 ECharts option。
- 图表 option 构造函数必须纯函数：输入数据，输出 option，不调接口。
- `BaseChart` 只封装 ECharts 生命周期，不写业务。
- 业务图表组件只组合数据和 option，不做复杂取数。
- 页面容器负责调 API 和管理 loading/error。
- 相同图表样式沉淀到 `shared/charts/chartOptions.ts`。
- 相同颜色、字体、tooltip 格式沉淀到 `chartTheme.ts`。

## 关联卡片

- [[HUB-质检前后端一体化学习与开发指南]]
- [[质检前后端一体化理想架构设计]]
- [[前端开发规范]]
- [[Vue3核心概念]]
- [[质检页签端到端开发流程指南]]
