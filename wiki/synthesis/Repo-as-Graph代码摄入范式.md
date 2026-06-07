---
title: "Repo-as-Graph代码摄入范式"
domain: ["knowledge_mgmt", "meta", "agent_engineering"]
type: "synthesis"
tags: [知识摄入, Ingest, Repo-as-Graph, 索引隔离, 代码检索]
created: 2026-06-07
updated: 2026-06-07
sources: 0
status: active
related_code: []
affects_path:
  - "skills/ai-librarian/SKILL.md"
trigger_keywords:
  - 代码摄入
  - Repo-as-Graph
  - 索引隔离法则
  - 动态读取
  - Ingest代码
---

# Repo-as-Graph代码摄入范式

## 🎯 解决的问题

直接把成百上千行的源代码直接作为知识卡片存储，会导致三个致命灾难：
1. **拓扑断裂**：代码是网状依赖的，按字数或标题分块会破坏函数调用链。
2. **高速过期**：代码天天在改，存在 Markdown 里的知识立刻沦为技术债。
3. **重点偏移**：代码已经完美诠释了 How，知识库最需要补全的是 Why，直接复制源码是舍本逐末。

## 🏗️ 核心解法：骨架提取 + 索引建卡 + 动态展开

本系统采用一种**“地图与实景分离”**的架构（索引隔离法则）：知识库仅作为代码的地图索引，不储存代码实景本身。

### 阶段 0：提取代码骨架 (Pre-process)
- 不让 Agent 读几万行的源码，而是运行 [[extract_code_skeleton脚本]]。
- 通过 AST 掏空所有实现细节，将代码降维为高密度、全依赖的“骨架 (Skeleton)”。

### 阶段 1：架构扫描 (Map)
- Agent 阅读骨架文件，梳理全盘逻辑，划分出核心模块边界（例如 `存储模块`、`网络模块`）。

### 阶段 2：索引建卡 (Reduce)
- Agent 为每个模块创建 `code_module` 卡片。
- 🚨 **强约束（索引隔离原则）**：卡片内**严禁**复制具体实现代码！卡片仅需包含三项：
  1. **Why**：该模块的设计意图和职责边界。
  2. **Who**：代码依赖关系（必须转化为卡片之间的 `[[双向链接]]`）。
  3. **Where**：填写 `related_code`（指向实际文件）并通过 `check_staleness.py` 绑定 `code_hash`。

### 阶段 3：运行时动态读取 (Live Query Phase)
- **这是实现闭环的关键**：当 Agent 处理后续任务、查图谱找到了这张 `code_module` 卡片时，发现带有 `related_code` 属性。
- 于是 Agent 调用其工具箱（如 `view_file` 或 `grep_search`），顺着 `related_code` 去实时读取**硬盘上最新鲜的真实源码**。

## 📊 设计借鉴

- **gbrain** 的上下文检索 (Contextual Retrieval)：先查语义概念，再顺着指针按需获取代码 AST。
- **Yuxi** 的定位窗设计 (`find_kb_document` + `open_kb_document`)：绝不通读全文，只根据索引精确定位后展开窗口。

通过这一范式，我们实现了：**图谱提供“全局架构地图”，卡片提供“导游解说”，文件系统提供“现场实景”。** 效率最高且永不过期。
