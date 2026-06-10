---
title: "CodeGraph解析层"
domain: ["code_intelligence"]
type: "code_module"
tags: [CodeGraph, resolution, import解析, 框架识别, 路径别名]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "codegraph/src/resolution/index.ts"
  - "codegraph/src/resolution/import-resolver.ts"
  - "codegraph/src/resolution/name-matcher.ts"
  - "codegraph/src/resolution/callback-synthesizer.ts"
  - "codegraph/src/resolution/frameworks/"
code_hash: ""
affects_path: []
trigger_keywords:
  - ReferenceResolver
  - import resolver
  - framework resolver
  - callback synthesizer
  - 框架识别
---

# CodeGraph解析层 (Resolution Layer)

## 职责

在 [[CodeGraph提取层]] 完成 AST 解析后，对提取的 import 引用和函数调用进行**跨文件解析**，将未解析的符号引用链接到具体的定义。

## 核心组件

- **ReferenceResolver** (`index.ts`)：解析编排器，协调所有子解析器
- **import-resolver.ts**：处理 import/require 路径解析
  - `path-aliases.ts`：支持 tsconfig paths / cargo workspace 路径别名
- **name-matcher.ts**：按名称匹配未解析引用
- **callback-synthesizer.ts**：[[动态调度桥接]]，合成回调/观察者/EventEmitter 边（全图 pass）

## 框架解析器 (Framework Resolvers)

每个框架解析器识别框架特有的模式并产生 `route` 节点和 `references` 边：

| 框架 | 文件 | 识别模式 |
|------|------|---------|
| Express | `frameworks/express.ts` | `app.get/post/put/delete(path, handler)` |
| Laravel | `frameworks/laravel.ts` | `Route::get`, Controller 方法 |
| Rails | `frameworks/rails.ts` | `resources :xxx`, `get/post` 路由 |
| FastAPI | `frameworks/fastapi.ts` | `@app.get`, `@router.post` 装饰器 |
| Django | `frameworks/django.ts` | `urlpatterns`, `path()`, ORM descriptor |
| Flask | `frameworks/flask.ts` | `@app.route` 装饰器 |
| Spring | `frameworks/spring.ts` | `@GetMapping`, `@PostMapping` 注解 |
| React Router | `frameworks/react-router.ts` | `<Route path=...>` JSX |
| SvelteKit | `frameworks/sveltekit.ts` | `+page.svelte`, `+server.ts` 约定 |
| Vue/Nuxt | `frameworks/vue-nuxt.ts` | `defineComponent`, Nuxt 文件约定 |

## 解析顺序

1. 提取阶段产出未解析引用（unresolved references）
2. `import-resolver` 解析 import 路径
3. `name-matcher` 按名称匹配剩余引用
4. 各 `FrameworkResolver.resolve()` 识别框架模式
5. `callback-synthesizer` 全图 pass 合成动态调度边

## 与其他层的关系

- 上游：处理 [[CodeGraph提取层]] 的未解析引用
- 输出：完善后的 edges 写入 [[CodeGraph存储层]]
- 下游：被 [[CodeGraph图遍历层]] 使用
