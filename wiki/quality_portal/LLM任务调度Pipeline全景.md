---
title: LLM任务调度Pipeline全景
domain: ["ai_dlc", "agent_engineering", "tooling"]
type: "synthesis"
tags: [质检平台, LLM任务调度, Pipeline, 状态机, 去重锁, 并发控制, 异常兜底]
created: 2026-06-21
updated: 2026-06-21
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: [Pipeline, 任务调度, 状态迁转, 通道, 去重锁, Dedup, Stage, TaskWorker, process_task, status聚合, OBS上传, 版本配置, 边界条件, 异常处理, fallback, 幂等, Watchdog, holder_id]
---

# LLM任务调度Pipeline全景

本卡是质检项目 LLM 数据生产与任务调度的中枢文档，覆盖状态迁转、6 通道拓扑、3 阶段调度、去重锁、数据表、OBS 上传、异常兜底和调度入口。

## 1. 总体拓扑

调度模式：

- Stage 1：`raw_img`、`label`、`pkl`、`prompt` 四通道并行。
- Stage 2：`video` 串行，依赖 Stage 1 中的 raw/label/pkl。
- Stage 3：`inference` 串行，依赖 video。
- Stage 间刷新 task 数据。
- 任一通道异常：写入通道失败，更新 `error_step`，停止后续阶段。

## 2. 双层状态架构

通道级状态是事实源：

- `raw_img_status`
- `label_status`
- `pkl_status`
- `video_status`
- `prompt_status`
- `inference_status`

任务级 `t_llm_task.status` 是派生字段，由 `_sync_task_status()` 自动聚合。

聚合优先级：

1. 任一通道 `failed` → 任务 `failed`
2. 全部通道 `completed` 或 `skipped` → 任务 `completed`
3. 任一通道 `running` → 任务 `running`
4. 否则 → `pending`

> ⚠️ 架构护栏：业务代码禁止直接写任务级 `status='completed'`，必须通过通道状态和 `_sync_task_status()` 派生。

## 3. 六通道职责

| 通道 | Stage | Handler | 业务实体 | OBS 上传 |
|---|---:|---|---|---|
| `raw_img` | S1 并行 | `_handle_raw_img` | `DataDownloader` / `ObsManager` | 有 |
| `label` | S1 并行 | `_handle_label` | `ObsManager` | 有 |
| `pkl` | S1 并行 | `_handle_pkl` | `ObsManager` | 有 |
| `prompt` | S1 并行 | `_handle_prompt` | 动态 processor import | 有 |
| `video` | S2 串行 | `_handle_video` | `VideoGenerator` | 有 |
| `inference` | S3 串行 | `_handle_inference` | `LLMInference` | 无，仅 `result_paths` |

统一 handler 模式：

1. 判断版本是否为 `-1`，是则写入 `skipped`。
2. 判断通道是否已 `completed`，是则幂等跳过。
3. 尝试获取去重锁或复用已有结果。
4. 执行业务逻辑并写入通道状态。

## 4. 去重锁体系

去重锁表是 `t_channel_dedup_lock`，核心字段：

- `dedup_key`：唯一键。
- `channel`：通道名。
- `producer_task_id`：生产者任务。
- `status`：锁状态。
- `holder_id`：持有进程标识。
- `result_data`：可复用结果。

dedup key：

| 通道 | 格式 |
|---|---|
| raw_img | `raw_img::{autosence_id}` |
| label | `label::{autosence_id}::{label_version}` |
| pkl | `pkl::{autosence_id}::{pkl_version}` |
| video | `video::{autosence_id}::{data_version}::{video_config_version}::{label_version}::{pkl_version}` |
| inference | `inference::{autosence_id}::{data_version}::{video_config_version}::{model_version}::{prompt_version}` |

`prompt` 通道不做去重锁。

治理机制：

- Graceful shutdown：`release_all_by_holder(holder_id)` 精准释放本进程锁。
- 启动时孤儿锁扫描：检测 holder 进程是否存活。
- Watchdog：周期清理超时锁和孤儿锁，默认 30 分钟。
- 数据库 UNIQUE 约束保证并发抢占只有一个生产者成功。

## 5. 数据表

`t_llm_task`：

- 业务键：`task_name`、`autosence_id`
- 版本字段：`data_version`、`label_version`、`pkl_version`、`video_config_version`、`prompt_version`、`model_version`
- 六通道状态与产物路径
- 任务级派生状态、错误信息、时间戳、优先级、重试次数
- `is_deleted` 软删除字段

`t_channel_dedup_lock`：

- `dedup_key` 唯一
- stale、orphan、holder 相关索引用于 Watchdog 和进程级清理。

`t_llm_version_config`：

- `version`
- `channel`
- `config` JSONB
- `processor`
- `processor_params` JSONB

## 6. OBS 上传

`_should_upload_obs(task, channel)` 读取各通道 `*_obs_upload_status` 判断是否上传。

覆盖范围：

- raw_img / label / pkl / video / prompt：有独立 OBS 上传状态列。
- inference：无 OBS 上传逻辑，只保留 `result_paths`。

上传状态流转：`pending -> uploading -> completed/failed`。

## 7. 关键边界条件

- `data_version`、`label_version`、`pkl_version`、`prompt_version` 为 `-1` 时，对应通道跳过。
- 已 `completed` 的通道必须幂等跳过。
- `VideoGenerator` 支持绝对时间戳优先，相对偏移 fallback。
- 复合视频整路缺失必须抛 `ValueError`，不应静默贴黑帧。
- 单帧缺失可向前搜索复制，最终补齐帧数。
- 帧丢失容忍阈值是 30%。
- 数据查询失败需要重试，典型间隔 5 秒、最多 3 次。
- 所有业务查询默认排除软删除：`WHERE is_deleted = FALSE`。

## 8. 调度入口

`TaskSchedulerApp` 支持：

- `--once`：单次执行后退出。
- `--daemon`：持续轮询。
- `--poll-interval`：默认 30 秒。
- `--limit`：单次拉取任务数，默认 10。

`run_once()` 流程：`fetch_pending_tasks(limit) -> process_task() -> exit`。

`run_daemon()` 流程：循环拉取、执行、sleep。

## 9. 关联卡片

- [[HUB-项目环境与开发规范总览]]
- [[HUB-前端与API层架构]]
- [[FastAPI后端API层架构]]
- [[TaskView交互流程详解]]
- [[VersionView版本配置页面交互详解]]
- [[质检一站式平台长期架构]]
