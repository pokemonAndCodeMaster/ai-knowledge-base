# The Anatomy of an Agent Harness（来自 LangChain）

> Source: https://blog.langchain.com/the-anatomy-of-an-agent-harness/
> Author: Vivek Trivedy (LangChain)

## 核心论点

**Agent = Model + Harness**

模型包含智能，Harness 使智能变得有用。我们正在构建的系统实际上需要一个工作引擎——能够持续完成任务的系统，而不仅仅是一次性的智能对话。

## Harness 的核心组成部分

### 1. State（状态）
- **短期记忆**：上下文窗口内的工作记忆。
- **长期记忆**：跨会话持久化的信息。
- **外部状态**：数据库、文件系统、API 中的状态。

智能体需要能够获取、更新并推理关于世界状态的信息。

### 2. Tool Execution（工具执行）
工具是 agent 与世界互动的方式。好的工具设计遵循：
- 最小化工具数量，最大化每个工具的表达力
- 防止工具失败级联成任务失败
- 工具结果需要对 LLM 可读

### 3. Feedback Loops（反馈循环）
Harness 需要将工具执行结果和环境变化反馈给 agent：
- 任务成功/失败信号
- 质量评分
- 错误消息（需要对 LLM 格式友好）

### 4. Enforceable Constraints（可执行约束）
- 不只是"建议"agent 遵循规则，而是机械地强制执行
- 类型检查、linters、结构测试，CI 检查
- 这些约束让 agent 更可控、更可预测

## 未来方向

随着 LLM 能力发展，Harness 中的某些组件可能变得不再必要（当模型可以自己处理时）。但 Harness 的整体价值在于它将"智能"转化为"可靠工作的系统"。
