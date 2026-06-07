# 统一知识系统维护法则 (Schema)

> **版本**：v3（2026-06-07 按 ai-librarian v2 Skill 规范重构，引入 TAXONOMY.yaml 双约束体系）
> **演进规则**：你（AI）与用户在实践中发现更好的模式时，主动提出修改此文件和 TAXONOMY.yaml。

---

## 🏛️ 目录结构约定

```
项目根/
├── TAXONOMY.yaml        # 分类法宪法（domain & type 枚举权威来源）
├── schema.md            # 本文件：命名规范、卡片模板、演进提案记录
├── index.md             # 全局知识黄页（单极目录，所有查询的起点）
├── log.md               # append-only 时序操作日志
├── raw/                 # 只读原始区（永远不要修改这里）
│   ├── articles/        # 原始文章
│   └── assets/          # 图片等附件
└── wiki/                # AI 完全拥有的编译区
    ├── sources/         # 每篇原始来源的精炼摘要（非全文复制）
    ├── entities/        # 实体卡片（人物、组织、产品、项目）
    ├── concepts/        # 概念卡片（理论、方法、术语、工具）
    └── synthesis/       # 综合分析页（跨多来源的对比/整合/框架）
```

---

## 📝 卡片 Frontmatter 规范（v3 完整版）

每张 wiki/ 下的 Markdown 文件**必须**包含以下 YAML Frontmatter：

```yaml
---
title: 卡片完整标题
domain: ["agent_engineering"]   # 必须是 List，取自 TAXONOMY.yaml domains 枚举
type: "concept"                  # 必须是 String，取自 TAXONOMY.yaml types 枚举
tags: [Agent, 工作流]             # 自由标签，便于 Obsidian Dataview 查询
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: 1                        # 引用来源数量（整数）
status: active                    # active | stale | superseded

# 正向锚定（我是谁的说明书？）
related_code: []                  # 对应的代码/配置文件路径（如无则留空列表）

# 反向护栏（我约束了谁？pitfall/norm 类型必须填写）
affects_path: []                  # 此卡片约束的路径模式
trigger_keywords: []              # 触发关键词（帮助 query 工作流快速联想到此卡片）
---
```

**来源摘要卡（sources/）额外包含：**
```yaml
source_url: https://...
source_type: article | twitter | youtube | github | gist | reddit
```

**旧版 Frontmatter 兼容说明**：存量卡片使用旧版字段（仅含 title/tags/created/updated/sources/status）时，ai-librarian 在更新这些卡片时应顺带补齐缺失字段，但**不要求一次性批量迁移**。

---

## 🔤 文件命名规范

- 文件名使用**小写中文或英文**，空格替换为下划线 `_`。
- 实体卡片：`entities/人名或组织名.md`（例：`entities/Andrej_Karpathy.md`）
- 概念卡片：`concepts/概念名.md`（例：`concepts/原子化笔记.md`）
- 来源摘要：`sources/简短英文标识.md`（例：`sources/karpathy_llm_wiki.md`）
- 综合分析：`synthesis/分析主题.md`（例：`synthesis/统一学习与知识管理框架.md`）

---

## 🔗 双向链接规范

- 使用 `[[文件名（不含路径和扩展名）]]` 格式。
- 跨目录链接时只写文件名，Obsidian 会自动解析。
- 链接类型标注（可选但推荐）：
  - `✅ 支持`：新内容印证此观点
  - `❌ 反驳`：新内容与此矛盾
  - `🔄 演化自`：此观点从另一观点发展而来

**双链焊死强制要求**（ai-librarian 执行 ingest 时必须遵守）：
- 新卡片创建后，必须找到源头卡片（相关 concepts、synthesis，或 index.md 对应分类）并在其末尾追加反向引用。
- pitfall/norm 类型卡片创建后，必须在所有 `affects_path` 中列出的文件或目录的说明卡末尾追加：
  `> ⚠️ 关联经验与规范：[[新卡片名称]]`

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

当出现以下情况时，ai-librarian 应主动提出更新 schema.md 或 TAXONOMY.yaml：
- 某类卡片频繁出现但缺乏对应 `type` 枚举值。
- 某个业务领域频繁出现但缺乏对应 `domain` 枚举值。
- 当前文件命名规范造成歧义或冲突。
- 某个标签体系需要扩展。

**演进提案格式**（记录在本文件末尾）：

```markdown
## 📋 待审批演进提案

### [YYYY-MM-DD] 提案：新增 type "experiment"
- 原因：实验记录频繁出现但缺乏对应规范
- 建议值：`experiment: "实验记录卡——假设、操作步骤、结果与结论"`
- 状态：待人类审批
```
