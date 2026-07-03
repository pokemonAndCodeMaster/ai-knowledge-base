# 📅 知识大脑动作流记录 (Log)

## [2026-06-21] update | 前后端一体化学习与开发指南 Hub

- **触发者**：用户希望把前后端一体化架构、ECharts、Router/API/View、可视化复用和页签端到端开发指南绑定到一张入口卡，并建立双向链接。
- **实施动作**：
  - 新增 `wiki/synthesis/HUB-质检前后端一体化学习与开发指南.md`。
  - 将 hub 与 `质检前后端一体化理想架构设计`、`ECharts从入门到掌握`、`Router_API_View与Python业务编排指南`、`前端可视化与组件复用工程指南`、`质检页签端到端开发流程指南` 建立双向链接。
  - 更新 `index.md` 注册 hub。

## [2026-06-21] synthesis | 前端可视化与页签端到端开发入门指南

- **触发者**：用户反馈理想化架构过抽象，希望补齐 ECharts、Router/API/View、前端可视化复用、单页签端到端开发的从入门到掌握指南。
- **新增卡片**：
  - `wiki/synthesis/ECharts从入门到掌握.md`
  - `wiki/synthesis/Router_API_View与Python业务编排指南.md`
  - `wiki/synthesis/前端可视化与组件复用工程指南.md`
  - `wiki/synthesis/质检页签端到端开发流程指南.md`
- **实施动作**：
  - 更新 `index.md` 注册四张指南。
  - 更新 `质检前后端一体化理想架构设计`，把操作指南接入理想架构入口。

## [2026-06-21] synthesis | 质检前后端一体化理想架构设计

- **触发者**：用户要求完整画出理想前后端一体架构，包括框架、组件、模块化、流程图、时序图、类图、代码层级、接口扩展、公共能力复用、设计模式与当前差距。
- **实施动作**：
  - 新增 `wiki/synthesis/质检前后端一体化理想架构设计.md`。
  - 设计内容覆盖总体架构图、后端分层、前端 feature slice、端到端时序、后端类图、API 设计、公共能力矩阵、设计原则与 P0-P3 演进路线。
  - 更新 `index.md` 与 `质检一站式平台长期架构` 的关联入口。

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

## [2026-06-07] upgrade | 知识库工业化升级：图索引检索系统

- **触发者**：用户要求将知识检索从手动遍历升级为工业级脚本驱动检索，参考 gbrain/Yuxi 开源项目
- **核心目标**：给定任务描述，一网打尽所有相关知识，token 消耗降低 75%

### 新增脚本工具链
- `scripts/compile_graph.py` — 图索引编译器（零外部依赖，纯正则解析 frontmatter）
- `scripts/query_graph.py` — 图检索查询器（Seed→Expand→Classify 三阶段算法）
- `scripts/check_staleness.py` — 过期检测器（code_hash 比对 + 孤岛/断链）
- `scripts/requirements.txt` — 零依赖声明

## [2026-06-21] update | NotebookLM MCP 配置与质检一站式平台知识整理

- **触发者**：用户要求安装配置 NotebookLM MCP，并摄入 `quality_check_pipeline` NotebookLM source，理解质检项目组当前工作与长期前后端架构。
- **MCP 配置**：
  - 新增 `tools/notebooklm-mcp/server.mjs`，复用本机已有 NotebookLM RPC client，暴露 `notebook_list`、`source_list`、`source_get_content`、`source_export_all`、`notebook_query`、`generate_artifact`、`studio_list` 等工具。
  - 新增 `tools/notebooklm-mcp/README.md`，记录认证、Codex 配置和 source 原文导出能力。
  - 已执行 `codex mcp add notebooklm -- node /home/yyh/project/ai-knowledge-base/tools/notebooklm-mcp/server.mjs` 注册 MCP。
- **知识整理**：
  - 重写并规范化 `wiki/quality_portal/` 下 7 张质检平台卡片，修复 NotebookLM 粘贴态内容缺少合法 Frontmatter 的问题。
  - 新增 `wiki/synthesis/质检一站式平台长期架构.md`，综合 LLM Pipeline、FastAPI、Vue3 前端与长期可维护架构路线。
  - 更新 `index.md`：新增长期架构综合卡，重写 Quality Check Pipeline 黄页摘要，移除已不存在的前端评估断链入口。
- **注意**：
  - 当前 NotebookLM MCP 协议层与本地配置已验证；NotebookLM 在线访问仍依赖 `~/.notebooklm-mcp/auth.json` 的 Google 登录会话，若会话过期需重新同步 cookie。

### 新增知识卡片（本次摄入）
- `wiki/synthesis/知识库工业化升级_图索引检索系统.md` — 完整技术总纲，含复现步骤
- `wiki/concepts/Seed_Expand_Classify检索范式.md` — 三阶段检索算法详解
- `wiki/norms/知识图谱编译与检索操作规范.md` — 编译时机/code_hash/trigger_keywords 规范
- `wiki/code/compile_graph脚本.md` — 编译器代码知识卡
- `wiki/code/query_graph脚本.md` — 查询器代码知识卡
- `wiki/code/check_staleness脚本.md` — 过期检测器代码知识卡

### 修改文件
- `TAXONOMY.yaml` — 新增 `code_module` 类型
- `schema.md` — 新增代码模块卡模板和写法原则
- `skills/ai-librarian/SKILL.md` — 工作流 A 改为三阶段脚本驱动，B 增加编译步骤，C 改为脚本驱动，新增工作流 E
- `index.md` — 注册所有新卡片，新增「操作规范」和「代码知识」两个分类区

### 验证结果（实测数据）
- 编译：55 卡片、220 链接、14 孤岛、71 断链（均自动检测）
- 查询 "设计多Agent系统"：21 张命中，full_read=3，token 估算从 ~50K 降至 ~13K（-75%）
- 查询 "高效学习新技术"：22 张命中，准确命中学习方法论全套卡片

## [2026-06-21] update | 质检一站式平台 src 骨架与 PostgreSQL 公共模块

- **触发者**：用户要求按质检项目组目录层级复刻当前项目，先还原 PostgreSQL 数据库模块，并为前后端一体架构演进打底。
- **实施动作**：
  - 新增 `src/config/`，以 `config/application.yaml` 为默认入口，支持环境变量占位和类型化 settings。
  - 新增 `src/database/`，实现 PostgreSQL 懒初始化连接池、查询/执行助手、健康检查和 `DatabaseManager`。
  - 新增 `src/api/`，实现 FastAPI `create_app()`、`deps.py`、`/api/health`、`/api/health/database` 与统一响应 schema。
  - 新增 `src/frontend/` feature slice 目录边界，以及 `src/llm/`、`src/data_check/`、`src/obs/`、`src/clipinfo/`、`src/pkl_vis/` 业务模块边界。
  - 新增 `requirements.txt` 与 `.env.example`，补充 `.gitignore` 运行产物规则。
- **知识沉淀**：
  - 新增代码卡：`配置管理公共模块`、`PostgreSQL数据库公共模块`、`FastAPI应用入口与依赖注入层`。
  - 更新 `质检一站式平台长期架构`，记录当前仓库第一阶段落地状态。
- **验证**：
  - `python -m compileall src tests`
  - `python -m unittest tests.test_config_database`
  - `python - <<'PY' ... create_app() ... PY`

## [2026-06-28] update | NotebookLM 全来源无损摄入 Skill 与经验固化

- 新增 `skills/notebooklm-source-ingest/`：完整导出与摄入流程、WSL2/Windows Chrome 认证和故障降级参考、Manifest/SHA-256 验证脚本。
- 新增 `wiki/norms/NotebookLM来源无损导出与摄入规范.md`，固化数量等式、浏览器下载字节门槛、认证安全、Map-Reduce 和结果报告口径。
- 更新 `wiki/concepts/notebooklm_mcp用法.md`：明确内容 RPC 会破坏 Markdown 结构，不得冒充原始文件。
- 更新 `wiki/synthesis/知识库高保真摄入管线.md`、`index.md`、`AGENTS.md` 并重编译图谱。

## [2026-06-28] ingest | NotebookLM quality_check_pipeline 完整摄入

- **触发者**：用户要求把 NotebookLM `quality_check_pipeline` 全部 source 完整导出为 Markdown，并完成知识卡、索引、双链和关联。
- **原始资料**：定位笔记本 `fc03a900-e886-44a5-85b0-73983c0efa41`，冻结 38 个 source 基线；通过已登录 Windows Chrome 原始下载链导出 38/38，失败 0，逐文件记录字节数、行数和 SHA-256。
- **重复项**：source 2=15、source 9=17 为字节级重复；原始文件全部保留，正文知识合并为 36 张卡。
- **知识编纂**：写入/更新 36 张完整正文卡，原始 Frontmatter 作为快照保留；新增 `notebooklm_quality_check_pipeline` 来源总卡。
- **防幻觉关系层**：原文共引用 146 个不同卡名；对未随笔记本提供原文的 102 个引用创建 `stale` 占位卡，明确 `[待人类补充]` 并焊接反向来源，新增 `quality_check_pipeline缺失引用索引`。
- **范围护栏**：来源描述上游 `e2e_data_pipeline_hub`；不存在于当前仓库的上游路径不写入有效 `related_code`，避免把来源快照冒充当前代码事实。
- **索引更新**：扩展 `index.md` 的来源、Raw、Quality Check Pipeline 总纲、LLM/前后端和人工质检十五步入口。

## [2026-06-07] upgrade | 知识库工业化升级：高保真摄入管线

- **触发者**：用户反馈单纯的 LLM 摄入经常丢失代码细节和参数边界
- **核心目标**：解决长文摄入时的 "Lost in the Middle" 现象，实现细节 100% 保真
- **实施动作**：
  - 新增脚本：`scripts/chunk_raw.py`，基于 Markdown 标题层级的 AST 分块器
  - 升级宪法：`schema.md` 新增 Direct Quote 护栏，禁止对具体技术细节进行概括
  - 重构流程：将 `SKILL.md` 中 `[ingest]` 升级为 Map-Reduce 两阶段模式（提取大纲 Checklist → 定向编纂）
  - 新增卡片：`知识库高保真摄入管线.md` 和 `chunk_raw脚本.md`

## [2026-06-07] upgrade | 知识库工业化升级：Repo-as-Graph 代码摄入管线

- **触发者**：用户提出将整个代码项目摄入知识库的需求
- **核心目标**：解决代码直接存入 Markdown 导致的“丢失调用链”、“上下文爆炸”与“极速过期”三大问题。
- **实施动作**：
  - 新增脚本：`scripts/extract_code_skeleton.py`（AST 骨架提取器，掏空实现细节，保留依赖拓扑与签名）
  - 升级工作流：在 `SKILL.md` 新增专属 `[ingest_code]` 工作流，确立“骨架提取 -> 架构扫描 -> 索引建卡 -> Hash 绑定”的标准管线。
  - 新增卡片：`Repo-as-Graph代码摄入范式.md`，确立了“知识库做索引导游，文件系统存源码实景”的设计哲学。

## [2026-06-10] deep-ingest | 5个开源项目深度摄入（codegraph + graphify + gbrain + Yuxi + agentscope）

- **触发者**：用户请求系统性摄入 5 个项目，目标是深度学习 AI 驱动的知识库管理、代码库智能管理、Agent 系统搭建
- **核心目标**：从上层架构、系统原理深入到底层实现，产出可复用的知识卡片体系
- **摄入方式**：
  - 代码类：`extract_code_skeleton.py` 骨架提取 → 架构扫描 → 模块建卡
  - 文档类：README + ARCHITECTURE + 设计文档 → entity + concept 建卡
  - 深度分析类：基于 `gbrain_yuxi_deep_analysis.md` (670行源码级分析) 直接建卡
- **产出统计**：31 张新增知识卡片
  - Entity × 5：CodeGraph / Graphify / gbrain / Yuxi / AgentScope
  - Concept × 11：Tree-sitter AST / 动态调度桥接 / Explore骨架化 / 搜索质量闭环 / 社区检测与Leiden / 混合模态提取 / RRF融合 / Dream Cycle / NamedThingBench / Atoms原子事实 / Agent权限系统 / Event驱动架构
  - Code Module × 10：CodeGraph 6层 / Graphify 管线 / gbrain检索层 / Yuxi检索层 / AgentScope工具层
  - Source × 5：4个项目文档来源 + 1个深度分析来源
- **更新文件**：`index.md` (全面扩充 4 个分类)
- **编译**：`compile_graph.py` 编译知识图谱，更新 `.wiki_graph.json`

## [2026-06-14] migrate | 重新迁移与完整集成 VLM/Qwen3.5 知识库 (基于正确路径)

- **触发者**：纠正源项目路径后，重新原封不动地完整迁移 `/mnt/d/project/llm_base/knowledge_base` 目录下的所有 Wiki 卡片与原始资料。
- **实施动作**：
  - **完整迁移 Wiki 卡片（共 34 张卡片）**：
    - **Concepts (共 27 张概念卡)**：
      - 视觉编码器与卷积组件：`navit_动态分辨率.md`、`conv3d_时空切块器.md`、`window_attention_交错注意力.md`、`swiglu_门控激活函数.md`、`rmsnorm_归一化.md`、`patchmerger_空间降维.md`、`vit_核心原理与结构.md`、`clip_对比学习视觉编码.md`、`convolution_卷积家族原理.md`
      - 位置编码：`2d_rope_视觉位置编码.md`、`mrope_多模态位置编码.md`、`qwen3.5_interleaved_mrope.md`、`rope_旋转位置编码.md`
      - Qwen 与多模态架构组件：`qwen3.5_混合decoder架构.md`、`qwen3.5_gated_delta_net.md`、`qwen3.5_视觉编码器.md`、`qwen3.5_多模态融合机制.md`、`qwen3.5_processor预处理.md`、`qwen3.5_文本嵌入与特殊token.md`、`llm_backbone_大语言模型基座.md`、`packing_物理隔离机制.md`、`qwen2.5_vl_预处理流水线.md`、`qwen2.5_vl_预处理框架集成与显存评估.md`、`qwen3.5_原生多模态训练范式.md`
      - 代码导航：`qwen_代码地图.md`
      - 架构对比：`动态分辨率方案对比.md`
      - 训练策略：`qwen2.5_vl_三阶段预训练.md`
    - **Sources (共 5 张来源卡)**：
      - `dynamic_resolution_动态分辨率.md`、`qwen2.5_vl_技术报告解析.md`、`qwen_evolution_架构演进与前沿底座.md`、`rope_系列原理解析.md`、`vision_foundation_视觉基石与卷积.md`
    - **Synthesis (共 2 张综合分析卡)**：
      - `qwen2.5_vl_深度剖析学习指南.md`、`qwen3.5_深度剖析学习指南.md`
  - **本地 `images/` 子目录完美保留**：
    - 完整保留 `wiki/concepts/images/` 和 `wiki/synthesis/images/` 下的所有图片资源，确保 Markdown 中的相对路径引用（如 `![](images/...)`）完全有效且在 Obsidian 等编辑器中显示正常。
  - **原始资料（共 25 个原始文件/目录）**：
    - 完整复制 `raw/` 目录下的 24 个文件/目录（包括多模态 3D-RoPE, SigLIP, SigLIP2, ViT 原始资料与模型显存分析等 Zip、Md 文件）以及根目录下的 `MCP_Guides/` 到 `raw/articles/`。
  - **更新文件**：
    - `index.md` — 重新组织「核心概念」、「来源摘要」、「原始材料总览」等表格分类，成功注册所有 34 张新卡片和 25 个原始资料。
    - `log.md` — 本条记录。
  - **编译索引**：
    - 运行 `compile_graph.py` 重新编译知识图谱，生成最新的 `.wiki_graph.json`。图谱成功编译：131 张卡片，501 个链接，无任何新生成的编译错误。
## [2026-06-28] update | 质检一站式平台 Phase 3 前架构接管评审

- **触发者**：用户提供 `task.md` 与 `implementation_plan.md`，要求接管任务、评估后端架构并规划下一步。
- **评审范围**：任务看板、实施蓝图、2 份 DDL、5 张阶段设计卡，以及当前 `src/api/`、`src/database/` 基建代码。
- **结论**：保留 feature slice、API/Service/Domain/Repository 分层、纯 Python 领域规则与代码注册表；Phase 3 前新增 Phase 2.5，先分离统计快照、任务级候选和操作台账，冻结预览/执行一致性、外部 Delta 幂等与失败恢复契约。
- **风险证据**：当前快照聚合行没有 task/clip 明细；结论与执行状态写入可重算读模型；表达式被写入表级 `UNIQUE` 约束；人员多项目与单一当前组语义冲突；共享 `repository.py` 会降低上下文内聚。
- **知识联动**：新增 `质检一站式平台Phase3前架构评审`，在 5 张相关设计卡补充反向评审链接，更新 `task.md` 和 `index.md`。
- **元数据校正**：三张尚未落地源码的方案卡由 `code_module` 校正为 `synthesis`，移除不存在的未来源码引用并补齐 `sources`，避免把设计稿伪装为当前代码事实。

## [2026-06-28] update | 质检平台第二轮架构收敛与 DDL 实跑

- **触发者**：用户逐项纠正第一轮评审，明确快照最小统计粒度、现有 Delta 状态回查机制、单项目人力约束和简洁架构偏好。
- **架构收敛**：撤回通用操作台账、`operation_id` 持久化、`ports.py`、`adapters/` 和集中式 `domain/` 目录建议；改为数据结构就近定义、复用后上移，共享 Repository 按表/数据源分小类，外部接口使用直白的 `delta_client.py`。
- **快照链路**：快照计算各最小单元采样配额；任务级中间表/Delta 表查询具体 task_ids；调用接口后通过任务状态回查刷新 `acceptance_allocated` 实际成功量。
- **人力与权限**：`projects TEXT[]` 改为单值 `project_name`；权限从每按钮布尔列收敛为每模块等级列。
- **DDL 验证**：在一次性 PostgreSQL 16.14 空实例顺序执行两份 migration，退出码均为 0；合法插入和联合键 UPSERT 成功，非法计数被 CHECK 约束正确拒绝；SQL 语法兼容基线声明为 PostgreSQL 10+。
- **联动更新**：修订 `task.md`、`implementation_plan.md`、三张核心设计卡、`src/manual_qc/acceptance/__init__.py`、评审卡、索引和图谱。

## [2026-06-28] ingest | 人工质检模块整体架构与组件知识树重编

- **触发者**：用户要求结合两轮讨论，形成可从总卡逐层 Review 的完整架构设计、组件分卡、双向链接和同步计划。
- **总入口**：新增 `wiki/synthesis/质检一站式平台人工质检模块整体架构.md`，覆盖范围、客观约束、组件图、验收分配/统计/通过打回三条链路、事实源、原则、开放问题和 Review 顺序。
- **新增分卡**：后端分层、API 契约、前端页面、Repository、Delta 状态回查、验收采样、通过打回、权限 SSO、实施路线与进度，共 9 张。
- **重构分卡**：`质检平台-采样与规则引擎设计` 改为 Hub，将采样和通过打回拆成两张原子叶子卡；完善快照、人力、数据结构、scene_name 和 Phase 3 前评审的总卡反链。
- **来源焊接**：人工质检 Hub、⑧验收分配、⑨批量通过打回、⑩状态刷新、⑪中间表更新和理想前后端架构均反向链接当前整体架构或对应组件卡。
- **计划同步**：`implementation_plan.md` 重写为 v4 当前实施契约；`task.md` 升级为 v4 动态看板，登记全部卡片、冻结决策、剩余外部信息和 Phase 3A～3E 顺序。
- **黄页**：`index.md` 新增整体架构入口，并完整注册当前人工质检增量设计知识树。
- **对账验证**：图谱编译为 314 张卡、1507 条链接；10 张本轮新增卡 Frontmatter/分类/物理证据/黄页/总卡双链检查 0 错误、0 新孤岛、0 新断链；并修正 `scene_name` 卡遗留的 NULL 汇总行 SQL。

## [2026-07-03] ingest | 人工质检交付中心与验收中心前端产品设计

- **触发者**：用户补充人工质检日常交付机制，明确一数据集一批次、需求对齐会、计划/实际到数、重点任务集合、定制行动项和表格/时间轴双视图。
- **业务机制**：新增 `人工质检-交付任务与行动项机制`，记录准备并行、规则培训/试标循环、生产与标注、验收打回返修，以及交付阶段/健康/行动项/验收结论四类状态分离。
- **交付中心**：新增 `质检平台-人工质检交付中心前端设计`，覆盖保存视图、需求对齐行内编辑、表格列预设、时间轴、单任务详情、三轨交付图和行动项面板。
- **验收中心**：新增 `质检平台-人工质检验收中心前端设计`，覆盖任务级总览、进度/质量/效率列视图、验收分配、验收监控、结果分析、结论执行和返修再验收。
- **联动更新**：重构 `质检平台-人工质检前端页面与状态设计` 为页面总览；更新人工质检整体架构总入口、`index.md` 和双向链接。
- **范围说明**：本轮只沉淀前端产品与业务机制，不假设后端接口、数据库字段或实现状态。
- **交互原型**：新增 `prototypes/manual-qc-demo/index.html`，用单文件 HTML/CSS/JavaScript 串起交付中心表格与时间轴、单任务三轨详情、行动项、验收总览及验收工作区；无需 Vue、构建工具或服务端即可直接打开。
- **原型边界**：所有任务、分配、结论与回查均为前端示例状态，不持久化，也不作为后端规则或数据库实现证据。

## [2026-07-03] ingest | Happy Coder 在 WSL2 中消息无响应排障

- **触发者**：用户反馈手机端显示已连接，但发送语音后 WSL2 与 Codex 均无响应。
- **本机证据**：`happy-coder 1.1.9` 成功初始化 `codex app-server` 并进入消息等待，随后 CLI 与 daemon 均出现中继 Socket 连接超时。
- **排障顺序**：先以新日志复现，再分别验证 HTTPS 与 Socket.IO，核对 WSL2 代理，网络正常后才清理会话、重绑或升级。
- **边界说明**：Codex 诊断沙箱中的 `/home` 为只读挂载，额外 `EROFS` 不能冒充用户普通 WSL2 终端的原始故障。
- **知识联动**：新增避坑卡并注册到工具实践类黄页；未修改 `raw/` 或 Happy/Codex 配置。

## [2026-07-03] update | Happy Coder 真实 WebSocket 路径与代理边界

- **新增证据**：用户的 HTTPS 请求通过 `https_proxy=http://127.0.0.1:7890` 成功访问中继首页；通用 `/socket.io/` 路径返回 404。
- **代码复核**：Happy Coder 1.1.9 固定使用 `path: "/v1/updates"`、`transports: ["websocket"]`，已安装代码未发现 WebSocket 代理 Agent 注入。
- **结论修正**：通用 Socket.IO polling 探针不适用于该版本；新增强制直连对照与真实 WebSocket Upgrade 探针。
- **修复方向**：若代理 HTTP 成功而直连超时，使用 Clash/Mihomo TUN 等透明代理；不要通过 `NO_PROXY` 强制中继直连。

## [2026-07-03] update | Happy Coder TUN 链路通过后的 Socket.IO 二分诊断

- **用户环境纠正**：Clash 已启用 TUN，WSL2 使用 Windows mirrored networking。
- **新鲜证据**：强制绕过显式代理后解析到 `198.18.1.166` 并成功完成 HTTPS；真实 `/v1/updates` WebSocket 请求返回 `101 Switching Protocols` 和 Engine.IO open 包。
- **边界收敛**：TUN、WSL2 出站、TLS、Cloudflare 与 WebSocket Upgrade 均正常，不再把“未开启透明代理”作为当前根因。
- **下一诊断**：使用 Happy 自带的 `socket.io-client` 和无效测试凭证连接；用明确认证错误与客户端 timeout 区分凭证/会话问题和 Node Socket.IO 传输问题。

## [2026-07-03] update | Happy Coder Node TLS 代理修复与双通道验证

- **最终根因**：同一 Clash Fake-IP 下 `curl` HTTPS 成功，但 Node 22.22.2 原生 `tls.connect` 与 Happy Socket.IO 均超时；显式注入 `HttpsProxyAgent` 后立即获得服务端认证响应。
- **实现**：新增 `scripts/happy_proxy_preload.cjs` 与 `scripts/happy-proxy`，只代理 Happy 中继域名，不修改全局 npm 包或 Happy 凭证；注册 `~/.local/bin/happy-proxy` 符号链接。
- **真实验证**：重启旧 daemon 后，Session Socket 记录 `Socket connected successfully`，Machine Socket 记录 `Connected to server`、keep-alive 启动及状态更新成功。
- **使用入口**：执行 `happy-proxy codex`；保留原始 `happy` 命令用于上游修复后的回归对照。

## [2026-07-03] update | happy-proxy 符号链接路径修复

- **原始症状**：通过 `~/.local/bin/happy-proxy` 启动时，包装器按符号链接目录查找预加载器，报 `Cannot find module '/home/yyh/.local/bin/happy_proxy_preload.cjs'`。
- **修复**：先用 `readlink -f` 解析包装器真实路径，再计算脚本目录与预加载器路径。
- **验证要求**：必须从 PATH 中的 `happy-proxy` 入口验证，不能只用仓库内绝对路径。
- **对账验证**：图谱编译为 317 张卡、1540 条链接；3 张新卡 Frontmatter 合法、均已登记黄页、0 新孤岛、0 新断链；聚焦查询可直接召回交付机制、交付中心、验收中心、前端总览和整体架构总入口。
