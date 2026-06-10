---
title: "NamedThingBench检索评测"
domain: ["knowledge_management", "evaluation"]
type: "concept"
tags: [NamedThingBench, 评测, Hit@1, MRR, CI门控, 检索质量]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "gbrain/src/eval/retrieval-quality/harness.ts"
affects_path: []
trigger_keywords:
  - NamedThingBench
  - 检索评测
  - Hit@1
  - MRR
  - CI门控
  - eval
  - hard-negative
---

# NamedThingBench检索评测

## 核心概念

NamedThingBench 是 [[gbrain项目]] 的 CI 级检索质量评测框架。它用预定义的测试用例来评估检索系统是否能正确召回目标文档，并设置硬门控阻止质量退化。

## 7 个测试族

> 引用自分析：

| 族 | 测试目标 | 门控要求 |
|----|---------|---------|
| title-substring | 标题包含查询词的页面能否排第一 | Hit@1 ≥ 95% （硬） |
| generic-to-named | 泛化查询能否定位到具体实体 | 软门控 |
| alias-synonym | 同义词/别名是否能匹配 | Hit@1 ≥ 98% （硬） |
| multi-chunk-dilution | 稀释在多 chunk 中的信息能否召回 | Hit@3 = 100% （硬） |
| short-vs-rich | 短小但精确的页面 vs 长但泛化的页面 | 软门控 |
| graph-relationship | 通过图关系能否发现间接关联 | 软门控 |
| hard-negative | 确保无关页面不出现在 top-3 | forbidden 页不出现 |

## 评测指标

> 引用自分析：

```typescript
for (const q of questions) {
    ranked = await searchFn(q.query);
    // Hit@1: firstRelevantIdx === 0
    // Hit@3: firstRelevantIdx < 3
    // MRR: 1 / (firstRelevantIdx + 1)
    // hard-negative: 验证 forbidden 页未出现在 top-3
}
```

## CI 硬门控

> 引用自分析：

```typescript
const DEFAULT_GATE = {
    hardFamilies: {
        'title-substring':      { hit_at_1: 0.95 },
        'multi-chunk-dilution': { hit_at_3: 1.0  },
        'alias-synonym':        { hit_at_1: 0.98 },
    },
    softFamilies: ['generic-to-named', 'short-vs-rich', ...],
};
// process.exit(gate.pass ? 0 : 1) → CI/CD 直接失败
```

## Harness 解耦设计

> 引用自分析：
> "harness 注入 SearchFn，完全解耦"

```typescript
const searchFn: SearchFn = async (q) => {
    const results = await hybridSearch(engine, q, { limit: 10 });
    return results.map(r => r.slug);
};
```

这意味着：
1. 评测框架不依赖特定检索实现
2. 换检索算法只需替换 `SearchFn`
3. 可以 A/B 测试不同检索策略

## 对知识库的启发

我们可以直接为知识库建立类似的 eval 体系：

```jsonl
{"family": "concept-lookup", "query": "什么是双向链接", "relevant": ["wiki/concepts/backlink.md"]}
{"family": "code-retrieval", "query": "TAXONOMY.yaml 的格式定义", "relevant": ["TAXONOMY.yaml"]}
{"family": "hard-negative", "query": "如何部署 Kubernetes", "forbidden": ["wiki/concepts/agent.md"]}
```

关键启发：**没有 eval 的检索系统是不可信的**。任何检索算法变更都必须过 eval gate。
