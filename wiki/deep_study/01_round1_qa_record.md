---
domain: [meta]
type: hub
status: active
created_at: 2026-06-14T07:11:36Z
updated_at: 2026-06-14T07:11:36Z
---

# 📝 第一轮深度问答与解读卡片生成记录 (Round 1 Q&A Record)

> **导航定位**：本归档卡片用于追踪 [学习路线总纲](wiki/synthesis/学习路线总纲.md) 中 P0 阶段核心模块的问答过程与生成产物，指导系统化知识库的高效沉淀。

---

## 🎯 问答概览

在第一轮学习中，我们针对 Agent 工程与多模态大模型（MLLM）在 **P0（基础与感知）** 领域的关键空缺进行了定向增强，完成了 2 张顶级工业水准的核心概念卡片生成。

---

## 📂 生成产物汇总

### 🛡️ Agent 工程领域
* **沉淀卡片**：[系统安全与沙箱隔离规范](wiki/concepts/系统安全与沙箱隔离规范.md)
* **核心内容**：
  - 设计了静态 AST Hook 扫描与黑白名单拦截、gVisor (RunSC) 容器隔离、CPU/Mem 资源配额以及 TTL 限时的三层防御纵深。
  - 制定了 `Bypass`/`Confirm`/`Deny` 三级鉴权状态机的人工确认门控 (HITL)。
  - 规定了敏感 Secrets 动态脱敏与日志过滤正则引擎。

### 🚗 多模态大模型领域
* **沉淀卡片**：[自动驾驶 MLLM Harness 架构设计](wiki/concepts/自动驾驶_mllm_harness_架构设计.md)
* **核心内容**：
  - 推演了从 **Perception Layer**（时空切块）到 **Action Harness Layer**（车辆物理安全包络）的五层时空对齐智驾架构。
  - 手写了基于 PyTorch 的完整仿真数据流闭环伪代码（包含 Conv3D 图像序列切分、MRoPE 时空编码融合、GatedDeltaNet 自回归控制决策和 Kinematic 安全硬门控）。

---

## 🔍 后续学习规划（Round 2 / P1 阶段）

随着 P0 阶段的核心搭建完毕，我们将在下一轮深度提问（Round 2）中转向 **P1（记忆与位置编码对齐）**。计划精读并生成以下卡片：

1. **Agent P1 核心**：
   - *MCP 协议与动态 Bridge 架构*：研究 MCP 服务器动态路由与上下文召回。
   - *Zettelkasten 式 Agent 向量与图混合记忆管理*。
2. **多模态 P1 核心**：
   - *三维 MRoPE 物理时间戳对齐推导*：结合 Qwen2.5-VL 源码分析三维旋转公式。
   - *GatedDeltaNet 线性注意力与 Full Attention 1:1 交替机制的参数流动*。
