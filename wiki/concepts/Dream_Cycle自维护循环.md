---
title: "Dream Cycle自维护循环"
domain: ["agent_engineering", "knowledge_management"]
type: "concept"
tags: [Dream Cycle, Autopilot, 自维护, gbrain, 守护进程]
created: 2026-06-10
updated: 2026-06-10
sources: 1
status: active
related_code:
  - "gbrain/src/commands/autopilot.ts"
affects_path: []
trigger_keywords:
  - Dream Cycle
  - Autopilot
  - 自维护循环
  - 夜间维护
  - brain_score
---

# Dream Cycle自维护循环

## 核心概念

Dream Cycle 是 [[gbrain项目]] 的知识库自维护机制——一个定时触发的维护循环，像人类大脑在睡眠中整理记忆一样，自动修复、丰富、优化知识库。

## 9 阶段流程

> 引用自分析：

```
Dream Cycle（每晚 cron 触发）：
  1. lint         → 格式检查
  2. backlinks    → 重建反向链接
  3. sync         → git → DB 增量同步
  4. extract      → 提取链接+timeline（增量，仅变更页）
  5. embed        → 生成/更新向量嵌入
  6. extract_atoms → 提取原子事实（可选）
  7. synthesize   → 合成 compiled_truth（跨页事实聚合）
  8. enrich       → 丰富实体信息（dedup/score/fix citations）
  9. score        → 更新 brain_score（脑健康度评分）
```

## Autopilot 智能调度

> 引用自分析：

```
每次 tick 先计算 remediation plan（cheap），再路由：
  ├─ Score ≥ 95 + plan 为空：每60min才做一次全周期
  ├─ 小 plan（≤3步，<5min）：提交单独 handler
  └─ 大 plan / 低分：提交完整 autopilot-cycle job（大锤）
```

## 保障机制

| 机制 | 说明 |
|------|------|
| 每个阶段独立 Job | 单阶段失败不影响其他阶段 |
| `gbrain-cycle` 全局锁 | 无并发冲突 |
| `autopilot.log` + audit JSONL | 全量审计 |
| `gbrain doctor` | 30+ 检查项的一键健康诊断 |
| ChildWorkerSupervisor | 5次崩溃上限 + 指数退避重启 |

## 对知识库的启发

这个模式直接映射到我们知识库的维护需求：

```
每周/触发：
  1. health check → 检查悬挂链接、缺失 frontmatter
  2. link extract → 重建双向链接索引
  3. eval run     → 跑完整 eval suite，报告分数变化
  4. contradiction check → 检查互相矛盾的知识卡片
  5. stale alert  → 标记超过 N 天未更新的高活跃卡片
```

关键启发：**知识库不是一次建好就完了，需要持续的自维护循环来保证质量不腐化**。
