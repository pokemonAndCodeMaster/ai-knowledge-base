---
title: "质检平台-scene_name概念"
domain: ["ai_dlc", "agent_evaluation"]
type: "concept"
tags: ["quality_check_pipeline", "scene_name", "任务组", "批次管理", "数据采集"]
created: 2026-06-28
updated: 2026-06-28
status: active
sources: 2
related_code: ["src/manual_qc/"]
affects_path: ["src/manual_qc/", "wiki/quality_portal/"]
trigger_keywords: ["scene_name", "任务组", "场景名", "批次", "clip", "最小管理单元", "任务粒度"]
---

# scene_name 概念说明

> scene_name 是人工质检流程中最重要的数据组织概念，理解它是理解整个质检流程的前提。

← [[质检一站式平台人工质检模块整体架构]] | [[人工质检-Hub]] | [[质检平台-综合快照表设计]]

→ [[质检平台-验收采样配额与任务选择设计]] | [[质检平台-通过打回规则与执行设计]]

> Phase 3 前评审保持本卡的层级定义：`scene_name` 是管理范围，`clip/task` 才是可采样、可执行，并可在重复操作前按任务状态检查的操作单元。见 [[质检一站式平台Phase3前架构评审]]。

## 1. scene_name 是什么

scene_name 是**上游送入人工质检的任务组（批次）的抽象标识**。

上游采集或挖掘数据时，一般一批数据会一起送到人工质检流水线，这一批数据：
- 通常是**同一类场景**（如城区直道跟车场景、VPD入库场景）
- 或者是**同一批次采集**（如某次采集活动的数据）
- 或者是**同一次挖掘**的数据（如某次从大库挖掘出的小样本）

这批数据进入 Delta 系统后，会统一挂在一个 **scene_name** 下，该 scene_name 就是这批数据的"任务组名"。

## 2. 最小管理单元

标注/验收的**最小操作单元**是 **clip（片段）**，每个 clip 是一条独立的标注任务（对应 Delta 中的一个 task）。

但**质检流程的最小管理单元**是 **scene_name**：
- 分配验收时，按 scene_name 来组织数据
- 统计通过率时，按 scene_name 来汇总
- 快照表中，scene_name 是主要维度键
- 批量通过/打回时，以 scene_name 为范围

```
scene_name: "城区高速_2026Q2_batch03"
    ├── clip_0001  → annotator: 张三 → behavior: A (Good)
    ├── clip_0002  → annotator: 张三 → behavior: B (Bad-行为1)
    ├── clip_0003  → annotator: 李四 → behavior: A (Good)
    ├── ...
    └── clip_2400  → annotator: 王五 → behavior: A (Good)
```

## 3. 与其他字段的关系

| 概念 | 存储字段 | 说明 |
|------|---------|------|
| scene_name | `scene_name VARCHAR(256)` | 任务组标识，来自 Delta 任务元数据 |
| clip | clip_id | 最小标注单元，多个 clip 属于同一 scene_name |
| task | Delta task_id | 在 Delta 系统中 task ≈ clip 的别名 |
| 标注员 | annotator_id → t_personnel | 一个 clip 只属于一个标注员 |
| 组 | group_name（来自 t_personnel.current_group）| 标注员所在组，用于按组聚合统计 |

## 4. 快照表如何使用 scene_name

`t_qc_daily_snapshot` 以 `(stat_date, scene_name, group_name, annotator_id)` 为联合唯一键。

典型查询场景：
```sql
-- 查某个 scene_name 下当天所有组的统计（从个人最小行聚合）
SELECT group_name,
       SUM(annotation_submitted) AS annotation_submitted,
       SUM(acceptance_allocated) AS acceptance_allocated
FROM t_qc_daily_snapshot
WHERE stat_date = '2026-06-28'
  AND scene_name = '城区高速_2026Q2_batch03'
GROUP BY group_name
ORDER BY group_name;

-- 查某个 scene_name 下所有标注员的个人统计（用于标注员画像）
SELECT * FROM t_qc_daily_snapshot
WHERE stat_date = '2026-06-28' AND scene_name = '城区高速_2026Q2_batch03'
ORDER BY annotator_id;
```

## 5. 在采样中的作用

采样时，GroupSampler 按 scene_name 比例分配抽取数量：

```
scene_name A 组下有 3 个 scene:
  city_batch01: 800 clips → 应抽 80/300 × total = 比例份额
  city_batch02: 1000 clips → 应抽 100/300 × total
  city_batch03: 1200 clips → 应抽 120/300 × total
```

即：确保每个 scene 都能被抽到，避免某个 scene 全部被跳过而没有验收。

## 6. 注意事项

> ⚠️ scene_name 是来自 Delta 的原始字段名，在部分历史代码和 Delta API 中也叫 `task_name`（含义相同，是上游任务组的名称）。在本项目中统一使用 `scene_name`。

> ⚠️ scene_name 不是 clip 的名字，也不是 Delta task_id。它是比 task 更高一层的"任务组"概念。
