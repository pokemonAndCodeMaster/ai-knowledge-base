# 🧠 知识大脑目录 (Index)

> 导航规则：先看📌总纲，再按需跳入对应分类。用 `grep "^## " index.md` 可快速显示所有分类标题。

---

## 📌 综合分析（Synthesis）

| 文件 | 摘要 |
|---|---|
| [统一学习与知识管理框架](wiki/synthesis/统一学习与知识管理框架.md) | 框架总纲：四步学习闭环（Ingest/Validate/Interrogate/Distill）+ 三层知识库架构的完整合体 |
| [Agent设计模式演进](wiki/synthesis/Agent设计模式演进.md) | 综合分析智能体设计模式从经典到前沿的演变，以及支撑这些模式的工程架构 |
| [Agent Harness Engineering 全景架构](wiki/synthesis/Agent_Harness_Engineering_全景架构.md) | 整合 7 篇权威文献，建立对 Agent Harness Engineering 的结构化认知：五层技术栈、8大原则、控制论框架、多 Agent 实践 |
| [Harness Engineering Roadmap (2026)](wiki/synthesis/harness_engineering_roadmap.md) | 2026 年 Harness Engineering 行业现状总结：AI-DLC、多 Agent 编排与 Repo-as-Agent 模式 |


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

### 🤖 AI 与智能体类

| 文件 | 摘要 |
|---|---|
| [Agent Engineering](wiki/concepts/Agent_Engineering.md) | 构建自主 AI 系统的工程学科，强调整体架构、约束和状态管理 |
| [Harness Engineering](wiki/concepts/Harness_Engineering.md) | 构建外围基础设施和约束以包围 AI 模型的新兴学科 |
| [Cognitive Gearing](wiki/concepts/Cognitive_Gearing.md) | 认知齿轮：在不同阶段切换 Agent 人设，强迫聚焦特定质量关卡 |
| [Agent Harness Engineering（综合）](wiki/concepts/Agent_Harness_Engineering.md) | Agent = Model + Harness；Harness 是差异化因素；8大核心原则 |
| [Harness Stack 分层架构](wiki/concepts/Harness_Stack_分层架构.md) | 从 Coding Agent 到全生命周期平台的五层技术栈，每层解决的核心问题 |
| [前馈与反馈控制](wiki/concepts/前馈与反馈控制.md) | Martin Fowler 框架：Guides（前馈）+ Sensors（反馈），计算型 vs 推理型 |
| [渐进式上下文披露](wiki/concepts/渐进式上下文披露.md) | AGENTS.md 是目录非百科全书；让 agent 按需递归发现上下文 |
| [Agent 工作流五大模式](wiki/concepts/Agent_工作流五大模式.md) | Anthropic 定义的可组合模式：提示链/路由/并行/编排-工作者/评估-优化 |
| [多 Agent 生成-评估循环](wiki/concepts/多Agent生成-评估循环.md) | GAN 启发：生成器+评估器分离，Sprint Contract，解决自我评估偏差 |
| [Context Reset vs Compaction](wiki/concepts/Context_Reset_vs_Compaction.md) | 两种解决 Context Anxiety 的策略对比；随模型演进选择不同方案 |
| [赛博控制论与 Harness](wiki/concepts/赛博控制论与Harness.md) | Harness 的哲学根源：Ashby 必要多样性定律、ACI 设计、控制回路 |
| [AI-DLC (AWS)](wiki/concepts/ai_dlc.md) | AWS 提出的 AI 驱动开发生命周期：从 Agile 转向 AI-Centric |
| [Mob Rituals](wiki/concepts/mob_rituals.md) | AI-DLC 下的团队仪式：Mob Elaboration (规划验证) 与 Mob Construction (协同构建) |
| [Bolts & Work Units](wiki/concepts/bolts_and_work_units.md) | 适配 AI 频率的组织原语：1-2 天的短冲刺 (Bolts) 与原子化任务 (UoW) |
| [Conductor vs Orchestrator](wiki/concepts/conductor_vs_orchestrator.md) | 人机交互的两种模式：单智能体实时指挥 (Conductor) vs 多智能体异步编排 (Orchestrator) |
| [GitAgent Pattern](wiki/concepts/gitagent_pattern.md) | Repo-as-Agent 设计模式：agent.yaml + SOUL.md + RULES.md 的声明式智能体定义 |
| [Harness Engineering Principles](wiki/concepts/harness_engineering_principles.md) | 汇总 OpenAI、Anthropic 等实践的 8 大核心原则：人类操盘、代码库为准、渐进披露等 |
| [Persistent Context](wiki/concepts/persistent_context_in_repo.md) | 将高保真需求与规格说明持久化在代码库中，作为智能体的"北极星" |


---
| [计算型与推理型 Harness](wiki/concepts/computational_vs_inferential.md) | 自动归档摄入 |
| [Steering Loop (控制回路)](wiki/concepts/steering_loop.md) | 自动归档摄入 |
| [Ashby's Law (必要多样性定律)](wiki/concepts/ashby_law.md) | 自动归档摄入 |
| [前馈与反馈控制 (Feedforward and Feedback)](wiki/concepts/feedforward_and_feedback.md) | 自动归档摄入 |


## 🏷️ 实体（Entities）

| 文件 | 摘要 |
|---|---|
| [Andrej Karpathy](wiki/entities/Andrej_Karpathy.md) | AI 研究者，前 OpenAI 联创，复利知识库（LLM Wiki）模式的提出者 |
| [Addy Osmani](wiki/entities/Addy_Osmani.md) | Google 高级工程领导，Agent-Skills 缔造者 |
| [Garry Tan](wiki/entities/Garry_Tan.md) | Y Combinator 总裁兼 CEO，Gstack 缔造者 |

---

## 📄 来源摘要（Sources）

| 文件 | 来源 | 摘要 |
|---|---|---|
| [Karpathy llm-wiki.md](wiki/sources/karpathy_llm_wiki.md) | GitHub Gist | LLM Wiki 架构理念原文；三层架构 + 三大操作的第一手论述 |
| [MIT 学生 48 小时速成](wiki/sources/mit_notebooklm_48h.md) | X（Twitter） | MIT 学生用 NotebookLM 48 小时掌握一门课的实践案例 |
| [Agent与Harness Engineering调研](wiki/sources/agent_and_harness_engineering_2026.md) | 2026调研报告 | 2026最新 Agent/Harness Engineering、工作流、系统及设计模式的深度总结 |
| [Awesome Agent Harness（README）](wiki/sources/awesome_agent_harness.md) | GitHub | 工具生态全景索引 + 8大原则 + 5个重要工具层 |
| [Martin Fowler：Harness Engineering](wiki/sources/martin_fowler_harness_engineering.md) | martinfowler.com | 赛博控制论框架；前馈引导+反馈传感器；可维护性/架构/行为三类 Harness |
| [Anthropic：Building Effective Agents](wiki/sources/anthropic_building_effective_agents.md) | Anthropic 研究博客 | 五种可组合 agent 工作流模式；简单性原则；ACI 工具设计 |
| [Anthropic：长时 Harness 设计](wiki/sources/anthropic_harness_design_long_running.md) | Anthropic 工程博客 | 三 Agent 架构（规划/生成/评估）+ Sprint Contract + Context Reset |
| [AWS：AI-DLC](wiki/sources/aws_ai_dlc.md) | AWS 官方博客 | AI 驱动开发生命周期全景：克服"步调差异"，重塑研发流程 |
| [Addy Osmani：Conductor to Orchestrator](wiki/sources/conductors_vs_orchestrators.md) | O'Reilly | 软件工程师角色的演变：从代码实现者转向多智能体交响乐的编排者 |


---

## 🔗 原始材料总览（Raw）

- 已从 NotebookLM（笔记本：AI 高效学习与知识管理法）导出 **30+ 篇**原始资料至 `raw/`
- 完整共 71 篇，持续补全中
- 主要涵盖：MIT学习法、费曼技巧、Karpathy llm-wiki、Obsidian Zettelkasten、NotebookLM 使用技巧等
- **2026-04-08 新增**：awesome-agent-harness 仓库 README + 5篇权威文献（Martin Fowler、Anthropic x2、LangChain、ignorance.ai）
| [2026 AI 智能体工程全景图](wiki/synthesis/2026_AI智能体工程全景图.md) | 自动归档摄入 |
| [Thoughtworks](wiki/entities/thoughtworks.md) | 自动归档摄入 |
| [Martin Fowler](wiki/entities/martin_fowler.md) | 自动归档摄入 |
| [Almirant (项目级 Agent 协调面板)](wiki/sources/almirant.md) | 自动归档摄入 |
| [Paperclip (零人类公司编排系统)](wiki/sources/paperclip.md) | 自动归档摄入 |
| [Martin Fowler：Harness](wiki/sources/martin_fowler_harness.md) | 自动归档摄入 |

