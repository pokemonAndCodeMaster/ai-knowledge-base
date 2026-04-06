# 📅 知识大脑动作流记录 (Log)

## [2026-04-06] init | 基础架构初始化
- 动作：成功建立 `llm_wiki` 基本存储架构体系 (`raw/`, `wiki/`)。
- 详情：引入了统一方法论大纲指南 `01_unified_master_guide.md` 并初步搭建好了 `schema.md` 以及根目录下的索引节点。
- 状态：准备开始从 NotebookLM 同步下载首批 71 篇源资料至 `raw/` 储备节点中。

## [2026-04-06] ingest | 工具实践：NotebookLM MCP 操作与知识库 Prompt 触发指南
- 动作：新增 2 张工具实践类原子知识卡片。
- 新增文件：
  - `wiki/notebooklm_mcp_用法手册.md` — nlm CLI 命令全集 + 批量导出脚本 + 注意事项
  - `wiki/ai知识库操作指南.md` — ai-librarian 三大操作 Prompt 模板 + 目录结构速查
- 更新文件：
  - `index.md` — 新增「工具实践类」分类并注册上述两张卡片
  - `wiki/01_unified_master_guide.md` — 新增「篇章三：工具实践层」，以 [[双向链接]] 关联上述两张卡片
- 触发者：用户请求整理 nlm 用法 + 教授如何触发 ai-librarian Skill

## [2026-04-06] migrate | 全库结构迁移：按 ai-librarian Skill v2 规范重构

- **触发原因**：ai-librarian SKILL.md 升级（补入 Karpathy 原文 + owenliang 实现），引入结构化子目录和 YAML Frontmatter 规范。
- **新建目录**：`wiki/sources/`、`wiki/entities/`、`wiki/concepts/`、`wiki/synthesis/`
- **迁移/新建文件（共 13 张卡片）**：
  - `wiki/synthesis/统一学习与知识管理框架.md`（原 `01_unified_master_guide.md` 重构为综合分析类）
  - `wiki/concepts/notebooklm_mcp用法.md`、`wiki/concepts/ai知识库操作指南.md`（原扁平文件迁移并更新）
  - 新建概念卡：`复利知识库`、`原子化笔记`、`双向链接`、`费曼学习法`、`MIT_48小时速成法`、`主动召回`、`间隔重复`、`RAG_vs_LLM_Wiki`
  - 新建实体卡：`entities/Andrej_Karpathy.md`
  - 新建来源摘要卡：`sources/karpathy_llm_wiki.md`、`sources/mit_notebooklm_48h.md`
- **更新文件**：
  - `index.md` — 全面重建为表格格式，四层分类（synthesis/concepts/entities/sources）
  - `schema.md` — 重写，加入 Frontmatter / 命名 / 链接类型 / log 格式规范
- **当前 wiki 状态**：1 synthesis + 9 concepts + 1 entity + 2 sources = 共 **13 张**知识卡片


