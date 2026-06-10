---
title: "gbrain_yuxi_source_analysis"
domain: ["agent_engineering", "knowledge_management"]
type: "source"
tags: [gbrain, Yuxi, 深度分析, 源码阅读]
created: 2026-06-10
updated: 2026-06-10
status: active
original_path: "gbrain/src/ + Yuxi/backend/"
content_hash: ""
---

# gbrain × Yuxi 深度技术分析来源记录

## 原文位置

### gbrain 核心文件
- `gbrain/src/core/search/hybrid.ts` (1871行, 混合检索核心)
- `gbrain/src/eval/retrieval-quality/harness.ts` (NamedThingBench)
- `gbrain/src/commands/autopilot.ts` (1541行, 守护进程)

### Yuxi 核心文件
- `Yuxi/backend/package/yuxi/knowledge/implementations/milvus.py` (1255行, 检索实现)
- `Yuxi/backend/package/yuxi/knowledge/chunking/ragflow_like/parsers/semantic.py` (语义分块)
- `Yuxi/backend/package/yuxi/agents/toolkits/kbs/tools.py` (知识库工具链)

## 分析维度

| 维度 | gbrain 方案 | Yuxi 方案 |
|------|------------|----------|
| 检索 | Vector+BM25+RRF+6阶段Boost (P@5 49.1%) | Milvus 内置 hybrid + PPR 图增强 |
| 摄入保真 | Atoms + compiled_truth | 语义分块 + title_path + 双写 |
| 准确性 | 矛盾检测 + NamedThingBench CI 门控 | LLM Judge 0/1 二分类 |
| 评测 | 7 族测试 + 硬/软门控 | Recall@K + F1@K + LLM Judge |
| 代码管理 | 分层检索 + Code 专属 eval | 5工具链（query/find/open） |
| 多 Agent | Minions Queue + Autopilot | LangGraph 中间件 + ARQ Worker |
| 维护循环 | Dream Cycle 9 阶段 | 解析→索引→检索 状态机 |

## 分解出的知识卡片
- [[gbrain项目]] / [[Yuxi项目]] (entity × 2)
- [[RRF融合与多阶段Boost]] / [[Dream Cycle自维护循环]] / [[NamedThingBench检索评测]] / [[Atoms原子事实提取]] (concept × 4)
- [[gbrain检索与合成层]] / [[Yuxi检索与知识图谱层]] (code_module × 2)
