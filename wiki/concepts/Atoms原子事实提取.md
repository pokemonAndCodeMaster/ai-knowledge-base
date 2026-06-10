---
title: "Atoms原子事实提取"
domain: ["knowledge_management"]
type: "concept"
tags: [Atoms, 原子事实, 信息保真, 知识摄入, compiled_truth]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "gbrain/src/"
affects_path: []
trigger_keywords:
  - atoms
  - 原子事实
  - extract_atoms
  - compiled_truth
  - 信息保真
  - 知识摄入保真
---

# Atoms原子事实提取

## 核心概念

Atoms 是 [[gbrain项目]] 解决"知识摄入信息丢失"问题的核心机制。将一个知识页面分解为原子级事实（每条事实独立可验证），然后独立存储和检索。

## gbrain 的实现

> 引用自分析：
> "**Atoms 提取**（`extract_atoms`）：从页面提取原子级事实，与 timeline 条目分开存储，避免信息丢失"

### 多层保真策略

| 层级 | 机制 | 说明 |
|------|------|------|
| L1 | Atoms 提取 | 原子级事实，独立存储 |
| L2 | 自动链接提取 | 零 LLM 调用，纯正则匹配 |
| L3 | Compiled Truth | 跨页事实聚合的合并版本 |
| L4 | Content Hash 去重 | SHA 短路已处理文件 |
| L5 | Stale Sweep | 扫描提取水印过期的页面 |

### Compiled Truth 工作流

```
页面 A → Atoms [a1, a2, a3]
页面 B → Atoms [b1, b2, b3]
          ↓
Dream Cycle → 发现 a2 和 b1 关联
          ↓
Compiled Truth（合并真相版本）：
  综合了 A 和 B 的相关原子事实
  chunk 时以 compiled_truth 为准
```

## Yuxi 的保真机制

> 引用自分析：
> "Yuxi 的分块在 flush 时带 `title_path`（标题链路，如 `# 第三章|第三节`）作为 chunk header"

Yuxi 的保真关键不在 Atoms，而在**结构化分块**：
1. 按 Markdown AST 智能切分
2. 表格整体一个 chunk
3. 代码块不切断
4. 每个 chunk 带 title_path 上下文
5. 超长 chunk 用 Embedding 相似度再切分

## 对知识库的启发

我们当前的知识摄入面临的核心问题：
- 信息缺失、不完整
- 过度省略、没有细节

解决方案参考：
1. **段级对账**：用 [ingest_audit] 对 原文段落 ↔ 卡片内容 做交叉对账
2. **原子事实清单**：每张卡片附加 `## 原子事实` 节，列出所有可验证的细粒度事实
3. **来源锚定**：每条事实标注 `> 引用自原文` + 原始文本

关键启发：**摄入时的信息保真比检索时的召回率更重要——丢失的信息永远无法被检索到**。
