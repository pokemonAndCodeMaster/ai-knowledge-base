# Building Effective Agents（原文存档）

> Source: https://www.anthropic.com/research/building-effective-agents
> Authors: Erik Schluntz, Barry Zhang (Anthropic)
> Published: Dec 19, 2024

## 核心论点

最成功的 agent 实现并非使用复杂框架或专门库，而是使用**简单、可组合的模式**。

## 关键定义

- **Workflows（工作流）**：LLM 和工具通过预定义代码路径协调。
- **Agents（智能体）**：LLM 动态指导自身过程和工具使用，自主控制完成任务的方式。

## 五种核心工作流模式

1. **Prompt Chaining（提示链）**：将任务分解为顺序步骤，每次 LLM 调用处理上一步的输出。适合可清晰分解为固定子任务的场景。

2. **Routing（路由）**：将输入分类并引导到专门的后续任务。适合有明显类别需区分处理的复杂任务。

3. **Parallelization（并行化）**：
   - Sectioning：将任务分解为独立子任务并行运行。
   - Voting：多次运行同一任务以获得多样化输出。

4. **Orchestrator-Workers（编排者-工作者）**：中央 LLM 动态分解任务，委托给 worker LLM，再综合结果。适合无法预测所需子任务的复杂任务。

5. **Evaluator-Optimizer（评估者-优化者）**：一个 LLM 生成响应，另一个提供评估和反馈，循环迭代。

## Agent 的三大核心原则

1. 保持简单的 agent 设计
2. 通过显式展示 agent 的规划步骤来优先考虑透明度
3. 通过全面的工具文档和测试来精心设计 agent-computer interface (ACI)

## Agent 的使用时机

- 开放性问题：难以或不可能预测所需步骤数量
- 无法硬编码固定路径
- 需要在可信环境中扩展任务（autonomy makes agents ideal for scaling）

## 工具设计最佳实践（Appendix 2）

- 给模型足够的 tokens 在"写进死角"之前先"思考"
- 格式尽量接近模型在互联网文本中自然见到的格式
- 确保没有格式"开销"（如需要准确计算代码行数）
- 把自己放在模型的角度考虑工具是否直观
- 使工具参数防错（Poka-yoke）

## 建议

- 从最简单的解决方案开始
- 只在确实能提升结果时才增加复杂性
- 在沙箱环境中进行广泛测试，配合适当的 guardrails
