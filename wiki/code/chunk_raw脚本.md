---
title: "chunk_raw脚本"
domain: ["knowledge_mgmt", "meta"]
type: "code_module"
tags: [AST分块, 语义分块, 预处理, 长文摄入]
created: 2026-06-07
updated: 2026-06-07
sources: 0
status: active
related_code:
  - "scripts/chunk_raw.py"
code_hash: "sha256:46bc3c6392ceef67"
affects_path: []
trigger_keywords:
  - chunk_raw
  - AST切分
  - 语义分块
  - 长文拆分
  - 预处理脚本
---

# chunk_raw脚本

## 职责（一句话）

将数万字的长篇 Raw 资料按 Markdown 标题层级（H1/H2）进行语义切分，并为每个分块注入上下文面包屑，解决 Agent 处理长文时的丢失细节问题。

## 运行方式

```bash
# 基本运行（默认输出到原文件同目录的 .chunks/ 子目录中）
python3 scripts/chunk_raw.py raw/articles/some_long_doc.md

# 指定输出目录
python3 scripts/chunk_raw.py raw/articles/some_long_doc.md temp_out/
```

## 关键函数与流程

```
chunk_markdown(filepath, output_dir)
  ├─ 逐行读取文件
  ├─ 识别 Markdown 代码块 (```)，避免切断代码
  ├─ 匹配 ^(#{1,2})\s+(.*) (识别 H1 / H2)
  │    └─ 遇到不在代码块内的 H1/H2，且已有累积内容，则触发切分
  └─ 写入文件
       └─ 在每个 Chunk 顶部注入：
          > 📍 来源文件: {name} | 语义分块: {i}/{total}
```

## 核心设计决策

1. **AST 语义感知**：并非按字数硬切断，而是按 Markdown 的 H1/H2 标题切断，保证每个 Chunk 在逻辑上是完整的独立章节。
2. **上下文面包屑**：在拆碎文件后，为防 Agent 产生幻觉，强制在文件首行加上原始文件名和分块进度，充当 `title_path` 的简易替代。
3. **零外部依赖**：为了方便集成，依然采用纯正则和标准库，不引入 `markdown-it` 等重型解析器。

## 与其他模块的关系

- 在 `ai-librarian` 的 `[ingest]` 工作流的第一步被调用。
- 替代了让大模型一次性读取全篇原文的做法，是实现**“高保真摄入管线”**（Map-Reduce 范式）的前置物理工具。
