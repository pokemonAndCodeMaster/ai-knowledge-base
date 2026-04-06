---
title: Karpathy LLM Wiki（llm-wiki.md）
tags: [来源摘要, Karpathy, 知识管理, LLM]
created: 2026-04-06
updated: 2026-04-06
source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
source_type: gist
status: active
---

# 来源摘要：Karpathy LLM Wiki（llm-wiki.md）

**作者**：[[Andrej_Karpathy]]
**发布时间**：2026 年 4 月
**Stars**：5000+（发布数小时内）

---

## 核心主张（摘要）

Karpathy 的这篇 gist 提出了一种个人知识管理的新模式，与传统 RAG 有根本区别：

1. **LLM 应持续编译知识，而非每次重新检索**：当新资料加入时，LLM 读取、提炼、整合进 Wiki，而不只是建索引。
2. **三层架构**：`raw/`（原始不可变）→ `wiki/`（LLM 编译）→ `schema.md`（约束法则）。
3. **三大操作**：Ingest（摄入）/ Query（查询）/ Lint（体检）。
4. **索引与日志**：`index.md` 是内容导航枢纽；`log.md` 是时序记录（append-only）。
5. **可选工具**：QMD（本地混合搜索）、Obsidian（图形化浏览）、Marp（幻灯片生成）。

---

## 关键引用

> "The wiki is a persistent, compounding artifact. The cross-references are already there. The contradictions have already been flagged."

> "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."

> "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."

---

## 引发的衍生实现

- [owenliang/llm-wiki](https://github.com/owenliang/llm-wiki)：结合 Obsidian + QMD 的完整实现
- ai-librarian Skill（本知识库正在使用的系统）：基于此模式构建

---

## 关联概念

[[复利知识库]] | [[RAG_vs_LLM_Wiki]] | [[原子化笔记]] | [[双向链接]]
