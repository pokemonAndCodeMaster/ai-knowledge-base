---
title: "CodeGraph提取层"
domain: ["code_intelligence"]
type: "code_module"
tags: [CodeGraph, extraction, Tree-sitter, AST, 语言提取器]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "codegraph/src/extraction/index.ts"
  - "codegraph/src/extraction/tree-sitter.ts"
  - "codegraph/src/extraction/tree-sitter-types.ts"
  - "codegraph/src/extraction/languages/"
  - "codegraph/src/extraction/parse-worker.ts"
code_hash: ""
affects_path: []
trigger_keywords:
  - extraction
  - 代码提取
  - ExtractionOrchestrator
  - LanguageExtractor
---

# CodeGraph提取层 (Extraction Layer)

## 职责

将源代码文件通过 Tree-sitter 解析为 AST，提取符号（nodes）和关系（edges），是 [[CodeGraph项目]] 管线的第一阶段。

## 核心组件

- **ExtractionOrchestrator** (`index.ts`)：调度所有语言的提取流程
- **tree-sitter.ts**：通用提取逻辑（extractMethod, extractCall, extractInheritance, extractVariable, extractField）
- **tree-sitter-types.ts**：`LanguageExtractor` 接口定义
- **languages/**：每种语言一个文件（如 `typescript.ts`, `python.ts`, `go.ts`）
- **parse-worker.ts**：将重型 AST 解析放到 Worker Thread 并行执行

## 关键接口

每个语言提取器需要实现的关键属性：
- `classTypes`, `functionTypes`, `methodTypes`：AST 节点类型映射
- `callTypes`：函数调用的 AST 节点类型
- `enumTypes`, `interfaceTypes`：结构化类型映射
- `getReceiverType?(node, source)`：获取方法的 receiver 类型（Go/Rust/Kotlin 需要）
- `visitNode?(node, ctx)`：自定义节点访问钩子
- `classifyClassNode?(node)`：区分 class/interface/enum/trait
- `resolveBody?(node)`：获取函数体（Kotlin 需要，因为 tree-sitter-kotlin 不用 field name）

## 特殊提取器

- **svelte-extractor.ts**：Svelte 单文件组件，`<script>` 委托给 TS/JS 解析，模板表达式单独扫描
- **vue-extractor.ts**：Vue SFC，script + script-setup 提取
- **liquid-extractor.ts**：Shopify Liquid 模板
- **dfm-extractor.ts**：Delphi DFM/FMX 表单文件

## 与其他层的关系

- 输出：写入 [[CodeGraph存储层]] 的 SQLite 数据库
- 后续：[[CodeGraph解析层]] 对提取的 import 引用进行解析和补全
