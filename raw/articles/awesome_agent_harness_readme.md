# awesome-agent-harness README（原文存档）

> Source: https://github.com/AutoJunjie/awesome-agent-harness
> Archived: 2026-04-08

A curated list of tools, frameworks, and resources for **agent harness engineering** — the discipline of designing environments, constraints, and feedback loops that make AI coding agents reliable at scale.

## What is an Agent Harness?

An agent harness is the infrastructure that wraps around an LLM coding agent. It's everything except the model itself: session management, context delivery, tool design, architectural enforcement, failure recovery, and human oversight.

OpenAI's Harness Engineering blog defined the term: *"When a software engineering team's primary job is no longer to write code, but to design environments, specify intent, and build feedback loops that allow agents to do reliable work."* Their team built 1M+ lines of production code with zero human-written lines using this approach.

Anthropic's Claude Code team discovered the same principles from the tool design side: the harness matters more than the model. Fewer, more expressive tools beat a long menu of narrow ones. Progressive disclosure — letting the agent recursively discover context across layers — outperforms loading everything upfront.

## Core Principles

1. **Humans steer, agents execute** — Engineers design environments and review outcomes, not write code
2. **Repository knowledge is the system of record** — If it's not in the repo, it doesn't exist to the agent. Slack threads, Google Docs, and tribal knowledge are invisible
3. **AGENTS.md is a table of contents, not an encyclopedia** — Point to deeper sources of truth; don't dump everything in one file
4. **Enforce architecture mechanically** — Custom linters, structural tests, and CI checks replace code review for invariants
5. **Agent legibility is the goal** — Optimize code for agent readability first, human readability second
6. **Fewer tools, more expressiveness** — Progressive disclosure and composable primitives beat sprawling toolkits
7. **See like an agent** — Read the model's outputs, watch where it struggles, and evolve the harness accordingly
8. **Corrections are cheap, waiting is expensive** — At high agent throughput, fix-forward beats blocking merge gates

## Full Lifecycle Platforms

- **Chorus** (github.com/Chorus-AIDLC/Chorus) — Agent harness for requirements-to-delivery. Task DAGs, sub-agent orchestration, human approval gates.
- **GitHub Agentic Workflows** — GitHub Actions with coding agent engines (Copilot, Claude Code, Codex).
- **Almirant** (almirant.ai) — Operating system for human-agent teams. Persistent context, shared memory, structured task lifecycle.
- **Paperclip** (github.com/paperclipai/paperclip) — Open-source orchestration for zero-human companies.

## Agent Orchestrators

- **Vibe Kanban** (github.com/BloopAI/vibe-kanban) — Kanban-based orchestrator with git worktree isolation per agent.
- **Emdash** (github.com/generalaction/emdash) — Agentic Development Environment (YC W26). Parallel agents in isolated worktrees.
- **Oh My Claude Code** (github.com/Yeachan-Heo/oh-my-claudecode) — Ultrapilot mode runs 5 Claude Code instances in parallel worktrees.
- **Composio Agent Orchestrator** — Plans tasks, spawns agents in isolated worktrees, handles CI fixes and merge conflicts.
- **Desplega Agent Swarm** — Multi-agent orchestration via task delegation, session continuity, shared memory.

## Task Runners

- **Symphony** (github.com/openai/symphony) — OpenAI's reference implementation. Polls Linear issues, spawns isolated Codex agents per task.
- **Baton** — Go implementation of Symphony.
- **Linear Coding Agent Harness** — Linear → autonomous coding agent → PR pipeline.
- **Axon** — Kubernetes-native framework. Apply a Task CRD, get back a PR.

## Agent Harness Frameworks

- **Deep Agents** (github.com/langchain-ai/deepagents) — Implements progressive disclosure through planning tools and subagent spawning.
- **DeerFlow 2.0** — ByteDance's SuperAgent harness. Skill system, sub-agent orchestration, sandboxed execution, persistent memory.
- **Zylos** — Persistent harness for Claude Code. Tiered memory, skill-based progressive disclosure.
- **Hive** — Outcome-driven agent framework. Queen agent generates agent graphs.
- **Meta-Harness** (yoonholee.com/meta-harness/) — Automated harness optimization using Claude Code.

## Agent Runtimes

- **OpenClaw** — AI agent runtime with skill system, sub-agent spawning, persistent session management.

## Agent Knowledge & Memory

- **claude-mem** — Automatic session capture with AI compression and injection into future sessions.
- **cq** — Enables AI coding agents to share learned knowledge across sessions.
- **Honcho** — Agent state memory library. Session history, user context, learned preferences.

## Coding Agents（主流）

Claude Code, Codex, OpenCode, Gemini CLI, Kiro CLI, Amp, Cursor, GitHub Copilot CLI, Aider, Warp AI

## Requirements & Spec Tools

- **Kiro IDE** — Spec-driven development IDE.
- **OpenSpec** — Spec-driven development CLI.
- **agents.md** (agents.md) — Open standard for project-level agent instructions.

## Standards & Protocols

- **MCP (Model Context Protocol)** — Open standard for connecting AI models to external tools.
- **AGENTS.md** — OpenAI's convention for repository-level agent instructions.
- **ACP (Agent Communication Protocol)** — Open protocol for agent-to-agent communication.
- **GitAgent** — Git-native standard: agent.yaml + SOUL.md + RULES.md.

## Methodologies & Workflows

- **AI-DLC Workflows** (github.com/awslabs/aidlc-workflows) — AWS's AI-Driven Development Life Cycle. Three-phase: understand → plan → build.

## Reference Articles

- Harness Engineering (OpenAI blog) — 1M+ lines with zero human-written code
- Lessons from Building Claude Code: Seeing Like an Agent (Thariq)
- Building Effective Agents (Anthropic)
- The Anatomy of an Agent Harness (LangChain)
- Harness Engineering (Martin Fowler) — Cybernetic governors model
- Harness Design for Long-Running Application Development (Anthropic)
- The Emerging "Harness Engineering" Playbook (ignorance.ai)
- Your Agent Needs a Harness, Not a Framework (Inngest)

## Reference Talks

- The Future of Coding is Agents — Andrej Karpathy (YC)
- Agentic Coding — Armin Ronacher
- 12 Rules of Harness Engineering
