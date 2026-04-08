# Harness Design for Long-Running Application Development（原文存档）

> Source: https://www.anthropic.com/engineering/harness-design-long-running-apps
> Author: Prithvi Rajasekaran (Anthropic Labs)
> Published: Mar 24, 2026

## 背景问题

- **上下文窗口满溢（Context Anxiety）**：模型在接近其认为的上下文限制时会过早结束工作。
- **自我评估偏差**：让 agent 评估自己的工作时，倾向于自我赞美，即使质量明显平庸。

## 解决方案：GAN 启发的多 agent 架构

将生成器（Generator）与评估器（Evaluator）分离，形成反馈循环。

**核心发现**：让独立 agent 进行批判，比让同一 agent 批判自己产出容易得多。一旦外部反馈存在，生成器就有具体的东西可以迭代改进。

## 前端设计实验

四个评分标准（生成器和评估器均使用）：
1. **Design Quality（设计质量）**：颜色、排版、布局、图像等是否创造了独特的情绪和身份认同
2. **Originality（原创性）**：是否有自定义决策，还是模板布局和 AI 模式？
3. **Craft（工艺）**：技术执行：排版层次、间距一致性、色彩和谐、对比度
4. **Functionality（功能性）**：可用性，独立于美学

**重要洞察**：标准措辞会以意想不到的方式引导生成器。包含"最好的设计是博物馆级别"会推动设计走向特定的视觉收敛。

## 全栈编码实验（三 agent 架构）

### Planner（规划者）
- 将简短的 1-4 句提示扩展为完整产品规格
- 关注高层次技术设计，而非详细实现
- 让下游 agents 决定实现路径，而非在规格中固化细节

### Generator（生成者）
- Sprint 制工作方式，每次实现一个功能
- 每个 sprint 结束后自我评估，再交给 QA

### Evaluator（评估者）
- 使用 Playwright MCP 像用户一样点击运行中的应用
- 针对 bugs 和标准对每个 sprint 评分
- 每个标准有硬性门槛，任意一项未达标则 sprint 失败

### Sprint Contract（Sprint 合同）
每个 sprint 开始前，生成器和评估器协商"完成"的定义，明确测试行为。

## Context Reset vs Compaction

- **Compaction（压缩）**：对较早的对话部分进行原位总结，同一 agent 继续工作。保留连续性，但 context anxiety 仍会持续。
- **Context Reset（上下文重置）**：完全清除上下文窗口，启动一个新 agent，通过结构化的 handoff 传递上一个 agent 的状态和下一步计划。提供干净的起点，但代价是 handoff artifact 需要足够的状态信息。

**关键发现**：随着模型持续改进，旧 harness 会出现"过度设计"。应定期重新评估 harness，去除不再"承重"的组件。

## 核心原则

1. 每个 harness 组件都编码了对模型无法独自完成的事情的假设，这些假设值得不断压力测试
2. 随着模型改进，有趣的 harness 组合空间不会缩小，而是在移动
3. AI 工程师的工作是持续找到下一个新颖的组合
