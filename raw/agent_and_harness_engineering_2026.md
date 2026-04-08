# 深度研究报告：Agent Engineering 与 Harness Engineering (2026最新前沿)

根据2026年的最新工程实践，Agent 领域已经从单纯的“提示词工程 (Prompt Engineering)”全面走向“智能体工程 (Agent Engineering)”与“外围脚手架工程 (Harness Engineering)”。以下是针对您的研究需求的深度总结与前沿材料。

## 1. 开源 Agent 工作流与 Skills 组

现代 Agent 正在摒弃“自由发挥”，转而采用高约束力的工作流（Skills）来保证工业级输出。

*   **[Addy Osmani's Agent-Skills](https://github.com/addyosmani/agent-skills)**
    *   **核心特性**：由 Google 高级工程领导 Addy Osmani 打造，为 Agent (如 Claude Code/Cursor) 引入生产级纪律。包含19个核心生命周期技能（`/spec`, `/plan`, `/test` 等）。
    *   **亮点实践 (Anti-Excuse 机制)**：其 SKILL.md 中硬编码了“反借口”表格（例如针对 AI 说“稍后添加测试”的借口，提供强制反驳逻辑），并通过“Verification-First（验证优先）”强制 Agent 在声明完成前必须给出测试通过的物理证据。
*   **Superpowers (本地拓展实践)**
    *   **核心特性**：一种强纪律性的本地拦截器工作流。通过 `/skills` 强制接管 AI 的初始思考路径。
    *   **亮点实践**：强制要求在写代码前激活 `brainstorming`、在执行前激活 `test-driven-development`。核心模式是将模糊需求物理拆解为精确的 `TodoWrite` 列表，是规范化 Agent 行为的最佳本地实践。
*   **Oh-My-OpenCode (现更名为 Oh-My-OpenAgent / omo)**
    *   **核心特性**：[code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) 是一个“自带电池”的高性能 Agent 挂载件，旨在打破底层大模型的 Vendor Lock-in。
    *   **亮点实践**：引入异步专属子 Agent 概念。例如 **Sisyphus** (负责死磕 Bug 直至解决)、**Prometheus** (负责架构规划) 和 **Council** (多模型投票决策)。同时集成了 LSP (语言服务器) 和 AST (抽象语法树)，实现了真正的代码级手术刀修改。
*   **Gstack (by Garry Tan)**
    *   **核心特性**：由 Y Combinator 掌门人打造的开源框架，旨在将 Claude Code 变成“虚拟工程团队”。
    *   **亮点实践 (Cognitive Gearing)**：通过“认知齿轮”机制在不同阶段切换 Agent 的人设（如 CEO、测试工程师、偏执型高级工程师）。例如在 `/review` 模式下，强制 Agent 停止生成新逻辑，仅寻找边界漏洞和架构缺陷。

## 2. 优秀的 Agent 系统与软件引擎

当前的 Agent 系统已经从“对话框”演进为后台守护进程和 TUI (终端用户界面) 平台。

*   **Claude Code**
    *   **定位**：Anthropic 官方出品的 CLI Agent，开创了现代终端 Agent 的交互范式。
    *   **特点**：通过 MCP (模型上下文协议) 深度集成文件系统与外部工具，是目前工程能力最强的闭源/半开源基座之一。
*   **OpenCode (anomalyco/opencode)**
    *   **定位**：开源、Provider-Agnostic 的终端优先 Agent ([GitHub](https://github.com/anomalyco/opencode))。
    *   **特点**：支持接入 OpenAI、Gemini 或本地 Ollama/Llama.cpp。内置极佳的终端 UI，并且可以直接在 GitHub 仓库中运行 `opencode github install`，将其配置为自动修复 Issue / PR 的自动化流水线。
*   **OpenClaw (前身为 Clawdbot)**
    *   **定位**：被称为 "Claude with hands" 的开源自动化代理框架 ([GitHub](https://github.com/openclaw/openclaw))。
    *   **特点**：Local-First 架构，作为后台守护进程运行。强项在于**多渠道通信**（Telegram, Discord, Slack 等集成），使得它不仅仅是一个代码助手，更是一个能执行真实世界任务的个人管家 Agent。

## 3. Harness Engineering (外围脚手架工程) 的优质材料与实践

**Harness Engineering** 的核心公式是：**Agent = Model (大脑) + Harness (身体与护栏)**。工程师不再花时间微调 Prompt，而是去写代码来物理限制 LLM 的行为。

*   **核心组件设计**：
    *   **Context Compaction (上下文压缩)**：防止长对话爆显存或导致 LLM “遗忘”。
    *   **State Persistence (状态持久化)**：利用 Git 工作流或文件系统解决大模型的“失忆症”。
    *   **Verification Loops (验证闭环)**：硬编码的脚本拦截器（如在 Agent 修改代码后，强制跑一遍 `tsc` 或 `pytest`，不通过则自动驳回要求重写）。
*   **业界优质实践材料**：
    *   **Anthropic 的三智能体护栏模式**：将“规划(Planning)”、“生成(Generation)”和“评估(Evaluation)”物理隔离，严防单个 Agent "既当裁判又当运动员"。
    *   **Stripe "Minions" 架构**：Stripe 内部的大规模 Agent 实践，其 Harness 设计确保了每周生成上千个安全的自动化 Pull Request，核心在于极其严格的沙盒测试护栏。
    *   **Datadog's Harness-First Engineering 博客**：提倡开发人员应将精力投资于编写“自动化验证拦截器”，让 Harness 去约束 Agent，而不是人工 Review 每一行 AI 生成的代码。

## 4. Skill / Agent 设计模式 (Design Patterns) 的优质实践

设计模式是构建复杂 Agent 的架构蓝图。

*   **经典基石模式 (Andrew Ng 提出)**：
    1.  **Reflection (反思模式)**：Agent 生成初稿 -> 执行 Critic 角色挑刺 -> 修正。高成本但极高质量。
    2.  **Tool Use (工具调用)**：赋予物理接口，杜绝幻觉（如遇到数学运算强制调用 Python 解释器）。
    3.  **Planning (规划模式)**：将复杂目标分解为可动态调整的 DAG（有向无环图）子任务。
    4.  **Multi-Agent Collaboration (多体协作)**：解耦复杂系统的利器，例如“架构师写 Spec + 码农写代码 + QA跑测试”。
*   **2026 前沿进阶模式**：
    *   **ReAct (Reason + Act)**：强制 Agent 输出 `Thought: [思考过程] -> Action: [工具调用] -> Observation: [环境反馈]` 的严格循环，大幅提高可解释性与调试效率。
    *   **Dynamic Routing (动态路由)**：前端为一个超轻量级意图识别 Router，根据任务类别将其路由到重型的专精型 Agent 组。
    *   **Human-in-the-Loop (HITL 拦截模式)**：Harness 层面的设计，在执行 `rm -rf`, `git push`, 或数据库 `DROP` 级操作时，挂起线程并请求终端人工干预。
*   **优质落地框架参考**：
    *   **LangGraph**：非常适合实现 Reflection 和 ReAct 这类带有循环 (Cyclic) 和强状态机流转的设计模式。
    *   **PydanticAI**：2025-2026 极其流行的框架，核心范式是利用类型系统 (Type safety) 和结构化输出约束 Agent 工具调用，属于典型的 Harness 强约束模式。
    *   **CrewAI**：最适合落地多智能体 (Multi-Agent Collaboration) 的框架，通过明确的 `Role`, `Goal`, `Backstory` 设计模式解耦逻辑。