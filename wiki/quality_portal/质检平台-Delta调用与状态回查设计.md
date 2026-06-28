---
title: "质检平台-Delta调用与状态回查设计"
domain: ["ai_dlc", "tooling", "agent_evaluation"]
type: "synthesis"
tags: ["人工质检", "Delta", "状态回查", "中间表", "外部接口", "最终一致"]
created: 2026-06-28
updated: 2026-06-28
sources: 8
status: active
related_code: ["task.md", "src/manual_qc/"]
affects_path: ["src/manual_qc/delta_client.py", "src/manual_qc/acceptance/services/"]
trigger_keywords: ["DeltaClient", "状态回查", "human_inspection_0920", "batch_assign", "batch_acceptance_pass", "task_rollback"]
---

# 质检平台 Delta 调用与状态回查设计

← 总入口：[[质检一站式平台人工质检模块整体架构]]。现状证据：[[人工质检-⑧验收分配]]、[[人工质检-⑨批量通过打回]]、[[人工质检-⑩状态刷新与GT回写]]、[[人工质检-⑪中间表更新]]。

## 1. 初衷与现状

Delta 是任务执行系统，本平台不能直接通过本地 SQL 修改其任务状态。当前人工质检脚本已经通过平台接口完成分配、送验收、通过和打回，并由后续 DAG 同步状态。

本设计的目标不是把这条链路改造成强一致事务，而是让前端能发起、看懂即时结果，并在稍后看到真实状态。

## 2. DeltaClient 边界

`src/manual_qc/delta_client.py` 集中封装：

```text
batch_assign(task_ids, acceptor, reviewer)
batch_review_pass(task_ids)
batch_acceptance_pass(task_ids)
task_rollback(task_ids)
```

它负责基址、认证 Header、超时、批量拆分、HTTP 错误解析和响应标准化；不负责采样、权限、统计或数据库写入。

真实 URL、认证字段、请求体和响应结构为 `[待人类补充]`，实现前必须从现有脚本或接口文档确认。

## 3. 已知现状链路

- 验收分配：待审核状态 66 `waiting_review` → `batch_assign` → `batch_review_pass`。
- 通过：`batch_review_pass` → `batch_acceptance_pass`，最终进入已完成。
- 打回：`task_rollback` 调两次，退回筛选；同时写现有 DMP 打回记录。
- 状态刷新：`human_inspection_refresh_status` 每 30 分钟同步 Delta 状态。
- 中间表：`human_inspection_update_middleware` 每 6 小时更新 `human_inspection_0920`，包含 task_id、task_name、acceptor、MergedTaskStatus、operate_time 等。

这些来自上游来源快照，当前仓库尚未有真实 Delta client 代码；实现时必须复核。

## 4. 为什么接口返回不等于最终成功

一次批量请求可能出现部分 task 已被处理、超时、接口返回成功但异步状态尚未落地等情况。因此区分：

- **请求量**：本次提交给接口的 task 数。
- **即时成功/失败**：接口响应能确认的结果。
- **实际成功量**：后续任务状态回查确认已进入目标状态的数量。

`t_qc_daily_snapshot.acceptance_allocated` 保存实际成功量，不保存纯请求量。

## 5. 分配后的回查

1. execute 前查询 task_ids 当前状态，只保留 waiting_review。
2. 调用 `batch_assign` 和必要的送验收接口。
3. 立即返回成功/跳过/失败摘要。
4. 用户手动刷新或定时任务查询 `human_inspection_0920`/Delta 状态。
5. 按日、scene、当日组、标注员重新聚合实际已分配数量。
6. UPSERT 快照 `acceptance_allocated`、Good/Bad allocated。

如果实际量低于 preview 预期量，页面显示差值，不把缺口静默当成成功。

## 6. 通过/打回后的回查

执行前根据目标动作过滤当前状态；已经处于目标状态的 task 记为 skipped。调用后由状态刷新确认：

- 通过目标：最终已完成；
- 打回目标：回到筛选/待重标状态；
- 未达到目标：保留为失败或处理中，允许稍后再查。

这就是本项目所需的“重复点击安全”：同一 task 不在合法前置状态时不重复调用，不引入额外幂等框架。

## 7. 配置与安全

- Delta 基址、超时、批大小、mock 开关进入 `src/config`。
- Token/密钥只从环境变量读取，禁止写入 Wiki、日志和前端。
- 日志记录接口名、task 数、耗时和错误摘要，不记录认证信息。
- 开发环境默认 mock 或只读；真实写接口必须显式配置启用。

## 8. 失败分类

| 类型 | 处理 |
|---|---|
| 参数/权限错误 | 调用前拒绝，不请求 Delta |
| task 状态已变化 | skipped 或冲突，返回当前状态 |
| 网络/超时 | 标为未知，先回查再决定是否重试 |
| Delta 明确失败 | 记录 task 级错误，只重试失败子集 |
| 本地快照刷新失败 | 不回滚 Delta；稍后从任务状态重新聚合 |

## 9. 验证门槛

- 使用 fake client 覆盖全部成功、部分失败、超时、重复 task。
- 集成环境验证状态值和两次 rollback 顺序。
- 证明实际量来自回查，而不是简单写入请求 task 数。

