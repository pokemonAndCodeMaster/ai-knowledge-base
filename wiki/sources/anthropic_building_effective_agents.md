---
title: Anthropic：Building Effective Agents
tags: [来源摘要, agent-design, 工作流模式, Anthropic]
created: 2026-04-08
updated: 2026-04-08
sources: 1
source_url: https://www.anthropic.com/research/building-effective-agents
source_type: article
status: active
---

# Anthropic：Building Effective Agents

**关联节点**：[[Agent 工作流五大模式]] | [[ACI（Agent-Computer Interface）]] | [[Agent Harness Engineering]] | [[Orchestrator-Workers模式]]

---

## 核心论断

> 最成功的 agent 实现并非使用复杂框架，而是使用**简单、可组合的模式**。

---

## 五种工作流模式（从简到繁）

| 模式 | 结构 | 适用场景 |
|---|---|---|
| **Prompt Chaining** | LLM → LLM → ... | 可清晰分解为顺序子任务的场景 |
| **Routing** | 分类器 → 专门处理器 | 有明显类别需区分处理的复杂任务 |
| **Parallelization** | 多 LLM 并行 → 汇总 | 独立子任务或需要多视角的任务 |
| **Orchestrator-Workers** | 中央 LLM 分配 → Workers | 无法预测子任务结构的复杂任务 |
| **Evaluator-Optimizer** | 生成器 + 评估器循环 | 有明确评估标准且迭代优化有价值的任务 |

---

## Agent 三大设计原则

1. **保持简单**：从最简单的解决方案开始，只在确实能提升结果时才增加复杂性
2. **优先透明**：显式展示 agent 的规划步骤
3. **精心设计 ACI**：agent-computer interface 需要与 HCI 同等关注度

---

## 工具设计建议（Appendix 2）

- 给模型足够 tokens 在"写进死角"之前先思考
- 格式贴近模型在互联网上自然见到的格式
- 确保无格式"开销"（不需要精确计算代码行数等）
- 站在模型的角度思考工具是否直观
- 使参数防错（Poka-yoke）

---

## 使用 Agent 的时机

- 无法预测所需步骤数量的开放性问题
- 无法硬编码固定路径
- 在可信环境中需要扩展任务规模

---

## 不使用 Agent 的时机

✅ 很多任务只需优化单次 LLM 调用 + 检索 + 上下文示例
