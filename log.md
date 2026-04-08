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

## [2026-04-06] ingest | 全景架构图 V3 (05_unified_infographic_v3_zh.png)
- **动作**：将架构图复制到 `raw/assets/` 并直接嵌入大纲文件。
- **新增文件**：`raw/assets/05_unified_infographic_v3_zh.png`
- **更新文件**：`wiki/synthesis/统一学习与知识管理框架.md`
- **触发者**：用户请求摄入指定图形到知识库

## [2026-04-07] ingest | Agent Engineering 与 Harness Engineering (2026最新前沿)
- 动作：将调研报告导入 `raw/`，并进行深度提取。
- 新增文件：
  - `raw/agent_and_harness_engineering_2026.md`
  - `wiki/sources/agent_and_harness_engineering_2026.md`
  - `wiki/concepts/Agent_Engineering.md`
  - `wiki/concepts/Harness_Engineering.md`
  - `wiki/concepts/Cognitive_Gearing.md`
  - `wiki/entities/Addy_Osmani.md`
  - `wiki/entities/Garry_Tan.md`
  - `wiki/synthesis/Agent设计模式演进.md`
- 更新文件：
  - `index.md` — 注册所有新卡片，新增「AI 与智能体类」分类
- 触发者：用户要求使用 ai-librarian 批量导入模式摄取报告

## [2026-04-08] ingest | awesome-agent-harness 仓库 + 7 篇权威文献

- **触发者**：用户请求拉取 github.com/AutoJunjie/awesome-agent-harness 的 README 及其引用文献
- **获取状态**：成功获取 5 篇文献（Martin Fowler、Anthropic x2、LangChain、ignorance.ai）；2 篇因 403 被限（OpenAI 博客、Medium）
- **新增 raw/ 文件（5 个）**：
  - `raw/articles/awesome_agent_harness_readme.md`
  - `raw/articles/martin_fowler_harness_engineering.md`
  - `raw/articles/anthropic_building_effective_agents.md`
  - `raw/articles/anthropic_harness_design_long_running.md`
  - `raw/articles/langchain_anatomy_agent_harness.md`
  - `raw/articles/ignorance_ai_harness_playbook.md`
- **新增 wiki/sources/ 文件（4 个）**：
  - `sources/awesome_agent_harness.md` — README 精炼摘要 + 工具生态全景
  - `sources/martin_fowler_harness_engineering.md` — 控制论框架权威参考
  - `sources/anthropic_building_effective_agents.md` — 五种可组合工作流模式
  - `sources/anthropic_harness_design_long_running.md` — 三 Agent 架构 + Sprint Contract
- **新增 wiki/concepts/ 文件（8 个）**：
  - `Agent_Harness_Engineering.md` — 领域综合定义与核心原则
  - `Harness_Stack_分层架构.md` — 五层技术栈
  - `前馈与反馈控制.md` — Guides + Sensors + 计算/推理型
  - `渐进式上下文披露.md` — AGENTS.md 作为目录的实现原则
  - `Agent_工作流五大模式.md` — Anthropic 五种可组合模式
  - `多Agent生成-评估循环.md` — GAN 启发架构 + Sprint Contract
  - `Context_Reset_vs_Compaction.md` — Context Anxiety 两种解法
  - `赛博控制论与Harness.md` — Ashby 定律 + ACI + 历史溯源
- **新增 wiki/synthesis/ 文件（1 个）**：
  - `synthesis/Agent_Harness_Engineering_全景架构.md` — 跨 7 篇文献综合分析
- **更新文件**：
  - `index.md` — 全面更新，新增 11 个概念卡条目、4 个来源摘要条目、1 个综合分析条目
  - `log.md` — 本条记录
- **当前 wiki 状态新增**：+8 concepts + 4 sources + 1 synthesis = 共 **新增 13 张**知识卡片

## [2026-04-08] synthesize | 深入 Harness 核心：AWS AI-DLC 与 Orchestration 模式

- **触发者**：在完成首批文献的基础上，进一步挖掘 AWS、Addy Osmani 以及 GitHub 社区的工程化实践
- **新增 raw/ 文件**：
  - `raw/articles/aws_ai_dlc.md` — AWS 官方 AI 生命周期博客
  - `raw/articles/conductors_vs_orchestrators.md` — Addy Osmani 关于智能体编排的文章
  - `raw/projects/gitagent_readme_full.md` — GitAgent 核心规约
  - `raw/projects/symphony_readme_full.md` — OpenAI Symphony 框架参考
- **新增/更新 wiki/sources/ 卡片**：
  - `sources/aws_ai_dlc.md` — AI-DLC 研发范式（Rituals, Bolts, Units）
  - `sources/conductors_vs_orchestrators.md` — Conductor (微观) vs Orchestrator (宏观)
- **新增/更新 wiki/concepts/ 卡片**：
  - `concepts/ai_dlc.md` — AI 驱动开发生命周期定义
  - `concepts/mob_rituals.md` — Mob Elaboration 与 Mob Construction
  - `concepts/bolts_and_work_units.md` — 适配 AI 速率的组织原语
  - `concepts/conductor_vs_orchestrator.md` — 两种人机协作范式对比
  - `concepts/gitagent_pattern.md` — Repo-as-Agent 设计模式 (SOUL.md, RULES.md)
  - `concepts/harness_engineering_principles.md` — 汇总 OpenAI/Anthropic 实践的 8 大原则
  - `concepts/persistent_context_in_repo.md` — 需求 spec 库内持久化原则
- **新增/更新 wiki/synthesis/ 卡片**：
  - `synthesis/harness_engineering_roadmap.md` — Harness Engineering 2026 行业现状与技术路线图
- **更新文件**：
  - `index.md` — 注册所有新增卡片
  - `log.md` — 本条记录
- **阶段性累计**：本轮新增 **2 sources + 7 concepts + 1 synthesis = 10 张**高质量卡片
## [2026-04-09] ingest | AI Librarain 自动整理与更新
- 动作：体检知识库 (Lint)，并将游离文件登记到 `index.md`。
- 详情：成功摄入并注册了 `2026_AI智能体工程全景图.md` 等 10 份新文件。
- 触发者：用户要求执行 lint、ingest 及 Git 提交。
