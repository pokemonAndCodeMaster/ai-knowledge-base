---
title: "codegraph_source_design_docs"
domain: ["code_intelligence"]
type: "source"
tags: [CodeGraph, design, 设计文档, CLAUDE.md]
created: 2026-06-10
updated: 2026-06-10
status: active
original_path: "codegraph/CLAUDE.md + codegraph/docs/"
content_hash: ""
---

# CodeGraph 设计文档来源记录

## 原文位置
- `codegraph/CLAUDE.md` (268 行)
- `codegraph/docs/SEARCH_QUALITY_LOOP.md` (559 行)
- `codegraph/docs/design/callback-edge-synthesis.md` (188 行)
- `codegraph/docs/design/adaptive-explore-sizing.md` (286 行)
- `codegraph/docs/design/dynamic-dispatch-coverage-playbook.md`
- `codegraph/docs/design/agent-codegraph-adoption.md`
- `codegraph/docs/benchmarks/call-sequence-analysis.md`

## 核心内容提炼

### CLAUDE.md：架构总览
- 管线：files → Extraction → DB → Resolution → Graph → Context → MCP
- NodeKind (22 种) × EdgeKind (12 种)
- Explore 预算分级：<500 files → 1 call, <5000 → 2, <15000 → 3
- 验证方法论：Agent A/B ≥2 runs/arm + 确定性 probe

### callback-edge-synthesis.md：动态调度桥接
- Field Observer（Phase 1） + EventEmitter（Phase 2） + 内联命名函数提取（Phase 3）
- 精度控制：fan-out cap = 6, 命名引用 only
- 实测：excalidraw 1/27k 合成边，precision 100%

### adaptive-explore-sizing.md：自适应骨架化
- 四条件判定：有 spine + 不在 spine + 多态兄弟(≥3 impl) + 未被特赦
- 6 个 Dead End（已验证无效的方案）
- 效果：OkHttp/Django 从成本异常值翻转为 ~10% 节省

### SEARCH_QUALITY_LOOP.md：语言验证指南
- 7 层 Test Battery 覆盖所有验证维度
- 15 种语言验证记录 + 每种语言的 AST 适配细节
- 故障诊断矩阵：44 个已知问题 → 修复位置映射

## 分解出的知识卡片
- [[动态调度桥接]] (concept)
- [[Explore自适应骨架化]] (concept)
- [[搜索质量闭环]] (concept)
