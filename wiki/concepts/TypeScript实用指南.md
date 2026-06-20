---
title: TypeScript 实用指南
domain: ["meta"]
type: "concept"
tags: [TypeScript, 前端, 类型系统, JavaScript]
created: 2026-06-19
updated: 2026-06-19
sources: 2
status: active
related_code: ["src/frontend/"]
affects_path: []
trigger_keywords: [TypeScript, 类型, interface, type, 泛型, any, unknown]
---

# 🔷 TypeScript 实用指南（Python 开发者视角）

> **定位**：为 Python 开发者设计的 TypeScript 速通指南。每个概念都有 Python 对照，聚焦实际项目中最常用的 20% 功能。
> **关联**：[[前端从零到精通学习指南]] | [[前端开发规范]]

---

## 1. TypeScript 是什么

TypeScript = JavaScript + 类型系统。

```
JavaScript:  动态类型，像 Python 一样灵活，但也一样容易出运行时类型错误
TypeScript:  静态类型，在你写代码时就告诉你类型错了，不用等到运行时才崩
```

**本质**：TypeScript 代码最终会被编译成 JavaScript 运行。类型标注只存在于开发阶段，编译后全部消失。就像 Python 的 type hints 在运行时不做任何检查，但 TypeScript 的编译器会强制检查。

---

## 2. 基本类型 — Python 对照表

```typescript
// ═══════════════════ TypeScript ═══════════════════    ═══ Python 对应 ═══

// 基本类型
const name: string = '张三'                             // name: str = '张三'
const age: number = 25                                  // age: int = 25（JS没有int/float区分）
const active: boolean = true                            // active: bool = True
const nothing: null = null                              // nothing: None = None
const notDefined: undefined = undefined                 // （Python没有undefined）

// 数组
const ids: number[] = [1, 2, 3]                         // ids: list[int] = [1, 2, 3]
const names: string[] = ['a', 'b']                      // names: list[str] = ['a', 'b']
const mixed: Array<string | number> = [1, 'a']          // mixed: list[str | int] = [1, 'a']

// 对象（用 interface，下面详解）
const task: LlmQcTask = { id: 1, name: '...' }         // task: LlmQcTask = LlmQcTask(id=1, name='...')

// 函数
function add(a: number, b: number): number {            // def add(a: int, b: int) -> int:
  return a + b                                          //     return a + b
}

// 可选参数（? 标记）
function greet(name: string, title?: string): string {  // def greet(name: str, title: str = None) -> str:
  return title ? `${title} ${name}` : name              //     return f"{title} {name}" if title else name
}
```

---

## 3. interface — 定义数据的"形状"

**Python 对照**：TypeScript 的 `interface` ≈ Python 的 `TypedDict` 或 `dataclass`。

```typescript
// 定义一个质检任务的数据结构
interface LlmQcTask {
  id: number                                            // 必填字段
  task_name: string
  model_name: string
  status: 'pending' | 'running' | 'completed' | 'failed'  // 联合类型（只能是这四个值之一）
  created_at: string
  updated_at: string
  assignee?: string                                     // ? 可选字段（可以有也可以没有）
  tags?: string[]                                       // 可选的标签数组
}

// Python 对应写法：
// class LlmQcTask(TypedDict):
//     id: int
//     task_name: str
//     model_name: str
//     status: Literal['pending', 'running', 'completed', 'failed']
//     created_at: str
//     updated_at: str
//     assignee: NotRequired[str]
//     tags: NotRequired[list[str]]
```

### interface 的继承和组合

```typescript
// 继承：扩展已有接口
interface TaskWithResults extends LlmQcTask {
  results: QcResult[]              // 添加新字段
  score: number
}

// 组合：从多个小接口组合
interface HasTimestamps {
  created_at: string
  updated_at: string
}

interface HasStatus {
  status: string
}

interface Task extends HasTimestamps, HasStatus {
  id: number
  name: string
}
```

---

## 4. 联合类型和字面量类型

```typescript
// 联合类型：可以是多种类型之一
let value: string | number = '张三'
value = 42    // ✅ 也可以是 number
value = true  // ❌ 不能是 boolean

// 字面量类型：只能是特定的几个值
type TaskStatus = 'pending' | 'running' | 'completed' | 'failed'
// Python 对应：Literal['pending', 'running', 'completed', 'failed']

let status: TaskStatus = 'pending'  // ✅
status = 'unknown'                  // ❌ TypeScript 编译器报错

// 在实际项目中的应用
function getStatusColor(status: TaskStatus): string {
  const colors: Record<TaskStatus, string> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
  }
  return colors[status]  // ★ TypeScript 能确保你处理了所有情况
}
```

---

## 5. 泛型 — 先会用，不急着创造

**类比**：泛型就像一个"模板"，让你写一个通用的类型，实际使用时再填入具体类型。

```typescript
// ── 你最常遇到的泛型场景 ──

// 场景 1：ref<T>()  —— 告诉 Vue 这个 ref 里存什么
const count = ref<number>(0)
const task = ref<LlmQcTask | null>(null)
const tasks = ref<LlmQcTask[]>([])

// 场景 2：API 响应类型
interface ApiResponse<T> {
  code: number
  message: string
  data: T         // T 是一个占位符，实际使用时替换
}

// 使用时指定 T 是什么
type TaskResponse = ApiResponse<LlmQcTask>
// 等价于：{ code: number, message: string, data: LlmQcTask }

type TaskListResponse = ApiResponse<PageResult<LlmQcTask>>
// 等价于：{ code: number, message: string, data: { items: LlmQcTask[], total: number, ... } }

// 场景 3：Axios 请求返回类型
request.get<any, PageResult<LlmQcTask>>('/api/v1/llm-qc/tasks')
//              ↑ 告诉 TypeScript 返回值的类型是 PageResult<LlmQcTask>
```

---

## 6. 类型断言和类型守卫

```typescript
// 类型断言：你比 TypeScript 更清楚类型是什么
const element = document.getElementById('chart') as HTMLDivElement
// 类似 Python 的 cast：element = cast(HTMLDivElement, document.getElementById('chart'))

// 类型守卫：运行时检查类型
function isTask(obj: unknown): obj is LlmQcTask {
  return typeof obj === 'object' && obj !== null && 'task_name' in obj
}

if (isTask(data)) {
  // 这个 if 块内，TypeScript 知道 data 是 LlmQcTask 类型
  console.log(data.task_name)
}
```

---

## 7. Record 和工具类型

```typescript
// Record<K, V>：创建一个键为 K 类型、值为 V 类型的对象类型
const statusLabels: Record<TaskStatus, string> = {
  pending: '等待中',
  running: '运行中',
  completed: '已完成',
  failed: '失败',
}

// Partial<T>：让所有字段变为可选
type PartialTask = Partial<LlmQcTask>
// 等于 { id?: number, task_name?: string, ... }
// 常用于更新操作：只传修改的字段

// Pick<T, K>：从 T 中选取部分字段
type TaskSummary = Pick<LlmQcTask, 'id' | 'task_name' | 'status'>
// 等于 { id: number, task_name: string, status: TaskStatus }

// Omit<T, K>：从 T 中排除某些字段
type CreateTaskParams = Omit<LlmQcTask, 'id' | 'created_at' | 'updated_at'>
// 创建时不需要 id 和时间戳（后端自动生成）
```

---

## 8. 在 Vue 中使用 TypeScript

### 8.1 组件 Props 类型

```typescript
// 推荐方式：使用泛型
const props = defineProps<{
  task: LlmQcTask
  editable?: boolean
}>()
```

### 8.2 Emits 类型

```typescript
const emit = defineEmits<{
  'update': [task: LlmQcTask]
  'delete': [id: number]
}>()
```

### 8.3 Ref 类型

```typescript
// 基本类型 ref（类型自动推导）
const count = ref(0)           // 自动推导为 Ref<number>
const name = ref('')           // 自动推导为 Ref<string>

// 复杂类型 ref（需要手动标注）
const task = ref<LlmQcTask | null>(null)     // 初始为 null，后续会赋值
const tasks = ref<LlmQcTask[]>([])           // 空数组需要标注元素类型

// 模板 ref（引用 DOM 元素）
const chartRef = ref<HTMLDivElement>()
const formRef = ref<InstanceType<typeof ElForm>>()
```

---

## 9. 常见错误和解决方案

```typescript
// ❌ 错误 1：使用 any
function process(data: any) { ... }
// ✅ 修复：用具体类型或 unknown
function process(data: LlmQcTask) { ... }
function process(data: unknown) { ... }  // 需要类型守卫后才能使用

// ❌ 错误 2：对象可能为 null
const task = ref<LlmQcTask | null>(null)
console.log(task.value.name)  // TS 报错：task.value 可能是 null
// ✅ 修复：先判断
if (task.value) {
  console.log(task.value.name)  // 安全
}
// 或者用可选链
console.log(task.value?.name)  // 如果 task.value 是 null，返回 undefined

// ❌ 错误 3：类型不匹配
const id: number = '123'    // TS 报错：不能将 string 赋给 number
// ✅ 修复：类型转换
const id: number = Number('123')
// 或从源头保证类型正确
```

---

## 10. import type 语法

```typescript
// 普通 import：导入值（运行时需要）
import { ref } from 'vue'
import { getTaskList } from '@/api/llmQc'

// type import：只导入类型（编译后会被删除，不增加打包体积）
import type { LlmQcTask } from '@/types/llmQc'
import type { Ref } from 'vue'

// ★ 规则：只用作类型标注的导入，必须用 import type
```

---

> ⚠️ 关联经验与规范：[[前端开发规范]]
> ✅ 支持：[[前端从零到精通学习指南]]
