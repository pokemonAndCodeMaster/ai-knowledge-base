# 统一知识系统维护法则 (Schema)

> **版本**：v2（2026-04-06 按 ai-librarian Skill 规范重构）
> **演进规则**：你（AI）与用户在实践中发现更好的模式时，主动提出修改此文件。

---

## 🏛️ 目录结构约定

```
llm_wiki/
├── schema.md          # 本文件：约束法则，随使用经验共同演进
├── index.md           # 全局知识目录（必须保持最新，每次 Ingest 后更新）
├── log.md             # append-only 时序操作日志
├── raw/               # 只读原始区（永远不要修改这里）
│   ├── articles/      # 原始文章（优先存放）
│   └── assets/        # 图片等附件
└── wiki/              # AI 完全拥有的编译区
    ├── sources/       # 每篇原始来源的精炼摘要（非全文复制）
    ├── entities/      # 实体卡片（人物、组织、产品、项目）
    ├── concepts/      # 概念卡片（理论、方法、术语、工具）
    └── synthesis/     # 综合分析页（跨多来源的对比/整合/框架）
```

---

## 📝 卡片 Frontmatter 规范

每张 wiki/ 下的 Markdown 文件**必须**包含以下 YAML Frontmatter：

```yaml
---
title: 卡片完整标题
tags: [分类标签, 主题标签]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: 引用来源数量（整数）
status: active        # active | stale | superseded
---
```

来源摘要卡（`sources/`）额外包含：
```yaml
source_url: https://...
source_type: article | twitter | youtube | github | gist | reddit
```

---

## 🔤 文件命名规范

- 文件名使用**小写中文或英文**，空格替换为下划线 `_`。
- 实体卡片：`entities/人名或组织名.md`（示例：`entities/Andrej_Karpathy.md`）
- 概念卡片：`concepts/概念名.md`（示例：`concepts/原子化笔记.md`）
- 来源摘要：`sources/简短英文标识.md`（示例：`sources/karpathy_llm_wiki.md`）
- 综合分析：`synthesis/分析主题.md`（示例：`synthesis/统一学习与知识管理框架.md`）

---

## 🔗 双向链接规范

- 使用 `[[文件名（不含路径和扩展名）]]` 格式。
- 跨目录链接时只写文件名，Obsidian 会自动解析。
- 链接类型标注（可选但推荐）：
  - `✅ 支持`：新内容印证此观点
  - `❌ 反驳`：新内容与此矛盾
  - `🔄 演化自`：此观点从另一观点发展而来

---

## 📅 log.md 格式规范

每条日志必须以 `## [YYYY-MM-DD] <操作类型> | <标题>` 开头，方便 grep 解析：

```bash
grep "^## \[" log.md | tail -5     # 查看最近5条操作记录
```

操作类型枚举：`init` | `ingest` | `query` | `lint` | `migrate` | `update`

---

## 🌏 语言约束

**所有 wiki/ 下的文件内容必须使用中文撰写**。即便原始资料是英文，摘要卡、概念卡的正文也需要翻译为中文。英文术语可保留原词，但解释文字必须是中文。

---

## 🔄 共同演进提示

当出现以下情况时，建议更新此 Schema：
- 某类卡片频繁出现但缺乏对应规范（如"实验记录"类）。
- 当前文件命名规范造成歧义。
- 某个标签体系需要扩展。
