---
title: "extract_code_skeleton脚本"
domain: ["knowledge_mgmt", "meta"]
type: "code_module"
tags: [AST分块, 骨架提取, 预处理, 代码摄入, Repo-as-Graph]
created: 2026-06-07
updated: 2026-06-07
sources: 0
status: active
related_code:
  - "scripts/extract_code_skeleton.py"
code_hash: "sha256:14a7b25439759ff1"
affects_path: []
trigger_keywords:
  - extract_code_skeleton
  - 代码骨架提取
  - 源码掏空
  - 剔除实现细节
  - 提取依赖
---

# extract_code_skeleton脚本

## 职责（一句话）

用于大规模代码库摄入预处理：通过 AST 或正则提取，掏空所有代码实现细节，仅保留文件结构、Import 依赖、类定义与关键函数签名，极致压缩 Token 消耗。

## 运行方式

```bash
# 提取整个项目/目录的代码骨架（默认输出到 .chunks/code_skeleton.md）
python3 scripts/extract_code_skeleton.py /path/to/project_src/

# 指定输出目录
python3 scripts/extract_code_skeleton.py scripts/ output_dir/
```

## 关键函数与流程

```
process_target(target_path, output_dir)
  ├─ os.walk 遍历目录，过滤隐藏文件与 __pycache__
  ├─ 根据后缀名路由
  │    ├─ Python 文件 (.py) -> extract_python_skeleton(f)
  │    │    └─ 使用原生 ast 库解析
  │    │    └─ 提取模块 Docstring、Import、ClassDef（含继承关系）和 FunctionDef
  │    │    └─ 完全忽略函数内部的逻辑节点
  │    └─ 通用文件 (.js, .ts, .go) -> extract_generic_skeleton(f)
  │         └─ 使用简单正则 (import|class|def|func) 提取特征行
  └─ 将所有提取的结构体组装为一份 .md 报告
```

## 核心设计决策

1. **分离细节（How vs Architecture）**：强迫 Agent 从“实现细节”拔高到“架构接口”视角。它把代码降维为骨架（Skeleton），Agent 据此编写只含 Why、Who、Where 的 `code_module` 卡片，而不会把代码贴进知识库里导致快速变质。
2. **多语言向下兼容**：优先用 Python 官方 `ast` 库实现 100% 准确的语法树提取，对其他语言采用防御性正则提取（Fallback）。
3. **零外部依赖**：为了轻量化，没有引入 `tree-sitter`，完全利用原生库，保证任意环境可开箱即用。

## 与其他模块的关系

- 该脚本是 **[[Repo-as-Graph代码摄入范式]]** 和 `[ingest_code]` 工作流的**物理前置工具**。
- 它生成的骨架文件是 LLM 进行“架构扫描 (Map)”的唯一输入。
