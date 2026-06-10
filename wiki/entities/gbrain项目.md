---
title: "gbrain项目"
domain: ["agent_engineering", "knowledge_management"]
type: "entity"
tags: [gbrain, Brain Layer, 个人知识库, MCP, Autopilot, Garry Tan]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "gbrain/src/"
affects_path: []
trigger_keywords:
  - gbrain
  - Brain Layer
  - brain engine
  - Garry Tan
  - autopilot
  - dream cycle
---

# gbrain项目

## 一句话定位

个人+团队 "Brain Layer" 系统：基于 TypeScript(Bun) 的 AI 知识合成平台，自动维护知识图谱，24/7 Autopilot 守护进程持续优化知识库质量。

## 生产规模

> 引用自分析：
> "146,646 pages, 24,585 people, 5,339 companies, 66 cron jobs"

## 核心架构：Thin Harness + Fat Skills

> 引用自分析：
> "`BrainEngine` 接口定义 ~47 个操作，两个引擎都实现 → **engine-agnostic**"

```
┌──────────────────────────────────────────┐
│  MCP Server (stdio/HTTP, 30+ tools)      │
│  ┌──────────────┐  ┌───────────────────┐ │
│  │ BrainEngine  │  │  Minions Queue    │ │
│  │ Interface    │  │  (Postgres-native) │ │
│  │ ~47 ops      │  │                   │ │
│  └──────┬───────┘  └────────┬──────────┘ │
│         │                   │            │
│  ┌──────▼───────────────────▼──────────┐ │
│  │         Brain Engine (Contract)     │ │
│  │  PGLiteEngine    │    PostgresEngine │ │
│  └─────────────────────────────────────┘ │
│                                          │
│  Skills (43 Markdown recipes)            │
└──────────────────────────────────────────┘
```

## 技术栈

- **语言**: TypeScript, Bun runtime
- **存储**: PGLite (个人, WASM Postgres17) / Supabase+pgvector (团队)
- **检索**: 混合检索（Vector HNSW + BM25 + RRF + Graph Signals）
- **通信**: MCP Server (30+ 工具)
- **后台**: Minions Queue (Postgres-native Job Queue) + Autopilot 守护进程

## 关键特性

1. **混合检索**：Vector + BM25 + RRF 融合 + 6 阶段 Post-Fusion Boost（实测 P@5 49.1%, R@5 97.9%）
2. **Dream Cycle**：夜间维护循环（lint → sync → extract → embed → synthesize → enrich → score）
3. **Autopilot**：智能调度守护进程，score < 95 触发完整修复周期
4. **NamedThingBench**：CI 级检索质量门控（title-substring Hit@1≥95%）
5. **Atoms 提取**：原子级事实提取，保证信息不丢失
6. **Compiled Truth**：跨页事实聚合的合并真相版本

## 与其他项目的关系

- 为 [[知识库工业化升级_图索引检索系统]] 提供了混合检索 Pipeline 的参考
- 与 [[Yuxi项目]] 形成互补：gbrain 侧重个人知识合成，Yuxi 侧重企业级多租户
