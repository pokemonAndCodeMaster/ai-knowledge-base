# 🧠 知识大脑目录 (Index)

> 导航规则：先看📌总纲，再按需跳入对应分类。用 `grep "^## " index.md` 可快速显示所有分类标题。

---

## 📌 综合分析（Synthesis）

| 文件 | 摘要 |
|---|---|
| [统一学习与知识管理框架](wiki/synthesis/统一学习与知识管理框架.md) | 框架总纲：四步学习闭环（Ingest/Validate/Interrogate/Distill）+ 三层知识库架构的完整合体 |

---

## 💡 核心概念（Concepts）

### 📚 学习方法类

| 文件 | 摘要 |
|---|---|
| [MIT_48小时速成法](wiki/concepts/MIT_48小时速成法.md) | 架构俯视→主动压测→矛盾探索的 AI 辅助高强度学习法 |
| [费曼学习法](wiki/concepts/费曼学习法.md) | 用"教给12岁孩子"来验证真正理解；AI 强化版可让 LLM 扮演挑剔学生 |
| [主动召回](wiki/concepts/主动召回.md) | 不看资料从记忆中提取信息，是记忆巩固效率最高的学习方式 |
| [间隔重复](wiki/concepts/间隔重复.md) | 在记忆快衰退时提醒复习；与主动召回组合成黄金学习搭档 |

### 🗂️ 知识管理架构类

| 文件 | 摘要 |
|---|---|
| [复利知识库](wiki/concepts/复利知识库.md) | LLM 持续编译维护 Markdown Wiki，取代无状态 RAG 的知识管理新模式 |
| [原子化笔记](wiki/concepts/原子化笔记.md) | 一卡一智：每张笔记只承载单一核心概念，是 Zettelkasten 的基石 |
| [双向链接](wiki/concepts/双向链接.md) | `[[页面名]]` 语法构建知识网络；类型化链接可标注支持/反驳/演化关系 |
| [RAG vs LLM Wiki](wiki/concepts/RAG_vs_LLM_Wiki.md) | 两种知识系统的根本差异：无状态检索 vs 有状态持续编译 |

### 🛠️ 工具实践类

| 文件 | 摘要 |
|---|---|
| [NotebookLM MCP 用法](wiki/concepts/notebooklm_mcp用法.md) | nlm CLI 完整命令速查 + 批量导出 Sources 脚本 + Studio/Research 功能 |
| [AI 知识库操作指南](wiki/concepts/ai知识库操作指南.md) | 如何用 Prompt 触发 ai-librarian 三大操作（Ingest/Query/Lint），含目录结构速查 |

---

## 🏷️ 实体（Entities）

| 文件 | 摘要 |
|---|---|
| [Andrej Karpathy](wiki/entities/Andrej_Karpathy.md) | AI 研究者，前 OpenAI 联创，复利知识库（LLM Wiki）模式的提出者 |

---

## 📄 来源摘要（Sources）

| 文件 | 来源 | 摘要 |
|---|---|---|
| [Karpathy llm-wiki.md](wiki/sources/karpathy_llm_wiki.md) | GitHub Gist | LLM Wiki 架构理念原文；三层架构 + 三大操作的第一手论述 |
| [MIT 学生 48 小时速成](wiki/sources/mit_notebooklm_48h.md) | X（Twitter） | MIT 学生用 NotebookLM 48 小时掌握一门课的实践案例 |

---

## 🔗 原始材料总览（Raw）

- 已从 NotebookLM（笔记本：AI 高效学习与知识管理法）导出 **30+ 篇**原始资料至 `raw/`
- 完整共 71 篇，持续补全中
- 主要涵盖：MIT学习法、费曼技巧、Karpathy llm-wiki、Obsidian Zettelkasten、NotebookLM 使用技巧等
