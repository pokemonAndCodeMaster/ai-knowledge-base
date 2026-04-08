---
title: Agent 工作流五大模式（Anthropic）
tags: [核心概念, agent-design, 工作流, 可组合模式]
created: 2026-04-08
updated: 2026-04-08
sources: 2
status: active
---

# Agent 工作流五大模式

**关联节点**：[[Agent Harness Engineering]] | [[anthropic_building_effective_agents]] | [[多Agent生成-评估循环]] | [[Orchestrator-Workers模式]]

---

## 设计哲学

> "使用简单、可组合的模式，而非复杂框架。只在确实能提升结果时才增加复杂性。"

---

## 五种模式（从简到繁）

### 1. Prompt Chaining（提示链）
```
Input → LLM₁ → [Gate] → LLM₂ → [Gate] → Output
```
- **适用**：任务可清晰分解为固定顺序子步骤
- **典型**：写大纲 → 检查 → 写正文；营销文案 → 翻译

### 2. Routing（路由）
```
Input → Classifier → 专门处理器A
                   → 专门处理器B
                   → 专门处理器C
```
- **适用**：输入有明显类别，各类别处理逻辑差异大
- **典型**：客服分流（一般查询/退款/技术支持）；按难度路由到不同大小的模型

### 3. Parallelization（并行化）
```
Input → LLM₁ ↘
      → LLM₂ → Aggregator → Output
      → LLM₃ ↗
```
两种变体：
- **Sectioning**：任务拆分为独立子任务并行执行
- **Voting**：同一任务多次执行取多数意见

### 4. Orchestrator-Workers（编排者-工作者）
```
Task → Orchestrator LLM → Worker₁, Worker₂, ... → Synthesizer
```
- **适用**：无法预测子任务结构的复杂任务（如修改多文件的代码任务）
- **关键**：与并行化不同，子任务不是预定义的，由 Orchestrator 动态决定

### 5. Evaluator-Optimizer（评估-优化循环）
```
Task → Generator → Output → Evaluator → [Pass? → 结束 : Feedback → Generator]
```
- **适用**：有明确评估标准，且迭代优化有价值
- **典型**：文学翻译的细腻度迭代；需要多轮搜索的复杂研究任务

---

## 使用决策树

```
任务是否能用单次 LLM 调用解决？
  ├── 是 → 优化单次调用（检索 + 上下文示例）
  └── 否 → 子任务是否可预测？
            ├── 是 → Prompt Chaining 或 Parallelization
            └── 否 → 是否需要动态分配？
                      ├── 是 → Orchestrator-Workers
                      └── 是否需要迭代优化？
                                └── 是 → Evaluator-Optimizer
```

---

## 与 Anthropic 长时 Harness 的关系

[[多Agent生成-评估循环]] 是 Evaluator-Optimizer 模式的生产级实现：
- Planner 负责初始分解（Orchestrator 角色）
- Generator 实现功能（Worker 角色）
- Evaluator 质检并反馈（Evaluator 角色）
- Sprint Contract 实现"可测试的完成定义"
