---
title: "CodeGraph同步与安装层"
domain: ["code_intelligence"]
type: "code_module"
tags: [CodeGraph, FileWatcher, 增量同步, 安装器, multi-agent]
created: 2026-06-10
updated: 2026-06-10
sources: 0
status: active
related_code:
  - "codegraph/src/sync/index.ts"
  - "codegraph/src/installer/"
  - "codegraph/src/bin/codegraph.ts"
code_hash: ""
affects_path: []
trigger_keywords:
  - FileWatcher
  - 增量同步
  - installer
  - multi-agent
  - codegraph install
---

# CodeGraph同步与安装层

## 同步子系统 (`src/sync/`)

### FileWatcher
- 使用原生 FSEvents (macOS) / inotify (Linux) / RDCW (Windows) 监听文件变更
- 2s debounce 防止频繁触发
- 支持 gitignore + 自定义 filter

### 增量同步流程
- `codegraph sync`：只重新解析变更的文件
- 基于文件 hash 比对，跳过未变更文件
- 全量索引：`codegraph init -i`

## 安装器子系统 (`src/installer/`)

### 多 Agent 安装架构

> 引用自原文：
> "adding a 5th agent is **one new file in `targets/` + one entry in `registry.ts`**"

支持的 Agent：
- **Claude Code** (`claude.ts`)：写入 `.mcp.json`
- **Cursor** (`cursor.ts`)：写入 `.cursor/mcp.json`，注入 `--path` 参数解决 cwd 问题
- **Codex** (`codex.ts`)：TOML 格式配置
- **opencode** (`opencode.ts`)：JSONC 格式，使用 `jsonc-parser` 保留用户注释

### 安装器设计要点

1. **幂等性**：重复安装不变更文件
2. **手术式编辑**：保留用户已有配置和注释
3. **标记清理**：用 `<!-- CODEGRAPH_START -->` / `<!-- CODEGRAPH_END -->` 标记管理旧版指令块
4. **单一真相源**：Agent 指导文本只在 `server-instructions.ts` 中维护，安装器不再写入指令文件

## CLI (`src/bin/codegraph.ts`)

子命令：`install`, `init`, `uninit`, `index`, `sync`, `status`, `query`, `files`, `context`, `affected`, `serve --mcp`

## 与其他层的关系

- 安装器是用户入口，配置好后启动 [[CodeGraph上下文层]] 的 MCP Server
- 同步子系统在文件变更时触发 [[CodeGraph提取层]] 的增量提取
