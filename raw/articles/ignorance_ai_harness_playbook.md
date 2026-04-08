# The Emerging "Harness Engineering" Playbook（ignorance.ai）

> Source: https://www.ignorance.ai/p/the-emerging-harness-engineering
> 副标题：从 OpenAI 到 Stripe 的 coding agents 最佳实践汇聚

## 核心来源

- OpenAI Harness Engineering 博客文章
- Stripe "Minions" 博客文章  
- OpenClaw 实践模式

## 核心 Playbook

### 仓库即真相来源（Repository As System of Record）
一切知识都必须在仓库中显式存在：AGENTS.md、skills/、规则文件。Slack 讨论、Google Docs 和口口相传对 agent 来说是不可见的。

### 渐进式上下文披露（Progressive Context Disclosure）
AGENTS.md 是目录，不是百科全书。指向更深的真相来源；不要把所有东西都堆在一个文件里。Agent 应该能够递归地跨层发现上下文。

### 机械强制架构（Enforce Architecture Mechanically）
用自定义 linters、结构测试和 CI 检查代替代码审查来强制执行不变量。

### 像 Agent 一样观察（See Like An Agent）
读取模型的输出，观察它在哪里挣扎，并相应地演化 Harness。

### 修正便宜，等待昂贵（Corrections Are Cheap, Waiting Is Expensive）
在高 agent 吞吐量下，fix-forward 模式比阻塞合并门更有效。

## Stripe 案例

Stripe 的 "Minions" 系统：
- 预推送钩子（pre-push hooks）：基于启发式运行相关 linters
- "蓝图"（blueprints）：将反馈传感器集成进 agent 工作流
- 强调"将反馈左移"（shift feedback left）的重要性

## 工具设计原则

- 更少的工具，更强的表达能力 > 大量狭窄工具
- 可组合的原语 > 固执己见的工作流
