---
title: "Explore自适应骨架化"
domain: ["code_intelligence", "agent_engineering"]
type: "concept"
tags: [CodeGraph, explore, 骨架化, 多态兄弟, 自适应输出, 检索优化]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "codegraph/src/mcp/tools.ts"
affects_path: []
trigger_keywords:
  - adaptive explore
  - 骨架化
  - sibling skeletonization
  - explore sizing
  - 多态兄弟检测
---

# Explore自适应骨架化 (Adaptive Explore Sizing)

## 解决的问题

当 Agent 问"请求如何通过拦截器链？"这类问题时，[[CodeGraph项目]] 的 `codegraph_explore` 工具会返回整个调用链上的所有源码。但如果链上有 14 个拦截器实现（如 OkHttp 的 Interceptor），返回 14 份几乎相同结构的完整源码会吃掉约 28KB 的上下文窗口——这比 Agent 自己用 grep/read 搜索还贵。

> 引用自原文：
> "So the whole game is: **tell 'interchangeable sibling' apart from 'distinct step,' cheaply.**"

## 核心算法

一个文件被骨架化（只显示签名，不显示函数体）当且仅当以下条件**全部**满足：

1. **存在 Flow Spine**：`buildFlowFromNamedSymbols` 成功构建了一条调用链
2. **不在 Spine 上**：该文件中没有任何符号位于 Flow 链上（链上节点始终保留完整源码）
3. **是多态兄弟**：文件中的类 implements/extends 了一个有 ≥3 个实现的超类型
4. **未被特赦**：Agent 没有在查询中命名该文件中的可调用符号（除非该文件自身定义了 ≥3 个实现的超类型）

## 效果验证

> 引用自原文：
> | Repo | WITH→WITHOUT cost | WITH reads | WITHOUT reads |
> |---|---|---|---|
> | **OkHttp** (n=4) | **$0.45 → $0.50** (~10% cheaper) | 2 | 3.5 |
> | **Django** (n=6) | **$0.56 → $0.63** (~10% cheaper) | 2 | 8.5 |

原本 OkHttp 和 Django 是 benchmark 中唯二的成本异常值（WITH 比 WITHOUT 还贵），经过自适应骨架化后双双翻转。

## Explore 预算分级

> 引用自原文：
> - `getExploreBudget(fileCount)` → call budget: `<500→1, <5000→2, <15000→3, <25000→4, ≥25000→5` (max 5)
> - `getExploreOutputBudget(fileCount)` → per-call output (chars / files / per-file)
> - **Invariant: 更大的 tier 永远不能比更小的 tier 分配更少的 `maxCharsPerFile`**

## 失败的尝试（Dead Ends）

这些方法被验证为无效，不要重试：

1. **降低低价值文件排名**：提升质量但不减小体积，explore 会用其他文件把释放的预算填满
2. **按入口节点过滤**：精确的符号查询会命名所有链参与者，导致没有任何东西被骨架化
3. **依赖 interface-impl 合成边做兄弟检测**：Kotlin 的 `fun interface` 没有被创建合成边
4. **"core-floor" 策略**（保留前 N 个完整，其余骨架化）：导致 Excalidraw +17% 成本回归
5. **Spare 家族文件**（因为定义了超类型就保留完整）：家族文件（2266 行）占满 28KB 预算，反而导致成本 +9%

## 对知识库检索的启发

这个设计验证了一个重要思路：**当检索结果的"冗余度"可以被结构性度量时（如 implements/extends 计数），可以自动化地压缩冗余**。这与我们的 [[知识库工业化升级_图索引检索系统]] 中 `classify` 阶段将卡片分为 `full_read`、`skim`、`skip` 的逻辑是同构的。
