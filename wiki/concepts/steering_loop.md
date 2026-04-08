---
title: 转向循环 (The Steering Loop)
tags: [概念, 智能体, 开发者经验]
created: 2026-04-08
updated: 2026-04-08
sources: [martin_fowler_harness]
status: active
---

# 转向循环 (The Steering Loop)

## 核心定义
在智能体软件工程中，人类开发者的主要工作发生了转移：**从“编写代码”转变为“迭代 Harness”**。

当智能体在某个任务上失败或犯错时，人类不应该只是帮它改代码，而是进入转向循环：
1. **分析错误**：为什么智能体没能做对？
2. **改进 Harness**：是前馈引导不足（提示词不够清晰）？还是反馈传感器缺失（漏掉了某个 Linter 规则或测试用例）？
3. **闭环治理**：将这次经验转化为持久化的 Linter 规则、文档或测试，防止智能体第二次犯同样的错误。

## 人类的职能转变
- **过去**：编写每一行逻辑。
- **现在**：作为“总编辑 (Editor-in-Chief)”或“系统设计师”，通过调整环境参数和约束条件来控制输出。

## 关联概念
- [[agent_harness]]
- [[feedforward_and_feedback]]
