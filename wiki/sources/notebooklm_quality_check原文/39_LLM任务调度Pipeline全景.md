---
title: "NotebookLM原文39-LLM任务调度Pipeline全景"
domain: ["knowledge_mgmt"]
type: "source"
tags: ["NotebookLM", "quality_check", "无损原文"]
created: 2026-07-04
updated: 2026-07-04
sources: 1
status: active
related_code: []
affects_path: []
trigger_keywords: ["quality_check", "NotebookLM原文", "LLM任务调度Pipeline全景"]
source_url: "notebooklm://6b4b949e-d423-4033-b16f-bd037ac03fa8/0da7cce6-c9a6-4e48-9296-9fb041b428ee"
source_type: "article"
---

# NotebookLM原文39-LLM任务调度Pipeline全景

## 来源追踪

- 来源总卡：[[notebooklm_quality_check_pipeline]]
- 原始文件：[原始 Markdown](../../../raw/notebooklm_exports/6b4b949e-d423-4033-b16f-bd037ac03fa8/39_0da7cce6-c9a6-4e48-9296-9fb041b428ee.md)
- source_id：`0da7cce6-c9a6-4e48-9296-9fb041b428ee`
- SHA-256：`d877b8d340b593b5f841ff9f2374189e8108bb1acf1a72def51b99019b649eff`
- 原始字节数：19783

## 原文（逐字符保留）

<!-- ORIGINAL_START -->
---
id: "SYN-LLM-PIPELINE-001"
title: "LLM任务调度Pipeline全景"
domain: ["llm_qa"]
type: "synthesis"

related_code:
  - "src/llm/scheduler.py"
  - "src/llm/task_repository.py"
  - "src/llm/task_creator.py"
  - "src/llm/task_query.py"
  - "src/llm/dedup_lock.py"
  - "src/llm/watchdog.py"
  - "src/llm/download.py"
  - "src/llm/video_generator.py"
  - "src/llm/video.py"
  - "src/llm/inference.py"
  - "src/llm/config.py"
  - "src/llm/formatter.py"
  - "src/llm/timing.py"
  - "src/llm/exceptions.py"

affects_path:
  - "src/llm/*"
  - "config/application.yaml"
  - "data_schemas/postgresql_relational/t_llm_task.sql"
  - "data_schemas/postgresql_relational/t_channel_dedup_lock.sql"

trigger_keywords: ["Pipeline", "任务调度", "状态迁转", "通道", "去重锁", "Dedup", "Stage", "TaskWorker", "process_task", "status聚合", "OBS上传", "版本配置", "边界条件", "异常处理", "fallback", "幂等", "Watchdog", "holder_id"]
tags: ["Pipeline全景", "状态机", "调度", "并发控制", "异常兜底"]
summary: "LLM 任务调度 Pipeline 的基础文档（central doc），涵盖完整的状态迁转机制、6 通道拓扑与实现、3 阶段调度模型、去重锁体系、数据表结构、OBS 上传架构、条件控制逻辑、边界条件处理、异常处理流程。后续所有 pipeline 相关知识以此为中枢进行关联和补全。"
---

# LLM 任务调度 Pipeline 全景

LLM 任务调度 Pipeline 的基础文档（central doc），涵盖完整的状态迁转机制、6 通道拓扑与实现、3 阶段调度模型、去重锁体系、数据表结构、OBS 上传架构、条件控制逻辑、边界条件处理、异常处理流程。后续所有 pipeline 相关知识以此为中枢进行关联和补全。

---

## 1. Pipeline 总体拓扑

```
                        ┌──────────────────────────────────────┐
                        │        TaskSchedulerApp (CLI)        │
                        │  --daemon / --once / --poll-interval │
                        └───────────────┬──────────────────────┘
                                        │ run_once() / run_daemon()
                                        ▼
                        ┌──────────────────────────────────────┐
                        │          TaskWorker.process_task()    │
                        │       (单任务 3 阶段 Pipeline)        │
                        └───────────────┬──────────────────────┘
                                        │
              ┌─────────────────────────┼─────────────────────────┐
              │                         │                         │
    ┌─────────▼──────────┐   ┌──────────▼──────────┐   ┌─────────▼──────────┐
    │  Stage1 (parallel)  │   │  Stage2 (sequential)│   │  Stage3 (sequential)│
    │  ThreadPoolExecutor │   │                     │   │                     │
    ├─────────────────────┤   ├─────────────────────┤   ├─────────────────────┤
    │ • raw_img           │   │ • video             │   │ • inference         │
    │ • label             │   │                     │   │                     │
    │ • pkl               │   │                     │   │                     │
    │ • prompt            │   │                     │   │                     │
    └─────────────────────┘   └─────────────────────┘   └─────────────────────┘
```

**调度模式**：Stage1 四通道并行（ThreadPoolExecutor），Stage2/Stage3 串行。Stage 间刷新 task 数据。通道异常 → `update_task_status("failed", error_step=channel)` + return。

---

## 2. 状态迁转机制

### 2.1 双层 status 架构

详见 [[任务级vs通道级status架构设计]]。

**通道级 status**（6 个 `*_status` 列）= 原始字段，由各通道 handler 独立写入。

**任务级 status**（`t_llm_task.status`）= 派生字段，由 `_sync_task_status()` 自动聚合。

> ⚠️ **禁止业务代码直接写 `status='completed'`**，必须通过 `_sync_task_status()` 派生。

### 2.2 通道 status 值域与迁转

```
pending → running → completed
                  → failed
                  → skipped (版本=-1)
```

| 场景 | 写入值 | 说明 |
|------|--------|------|
| 版本=-1 跳过 | `skipped` | `repo.update_channel_status(task_id, "raw_img", "skipped")` |
| 通道已 completed 幂等跳过 | 不写入 | `task.get("label_status") == "completed"` → return |
| 通道开始执行 | `running` | `repo.update_channel_status(task_id, "raw_img", "running")` |
| 通道执行成功 | `completed` | `repo.update_channel_status(task_id, "raw_img", "completed", local_path=...)` |
| 通道执行失败 | `failed` | `repo.update_channel_status(task_id, "raw_img", "failed")` |

### 2.3 任务级 status 聚合规则

`_sync_task_status()` SQL CASE 表达式，按优先级：

1. 任一通道 `failed` → 任务 `failed`
2. 全部通道 `completed` 或 `skipped` → 任务 `completed`
3. 有通道 `running` → 任务 `running`
4. 否则 → `pending`

触发时机：`update_channel_status()` 末尾自动调用。

---

## 3. 6 通道详细实现

### 3.1 通道总览

| 通道 | handler 函数 | Stage | 业务实体 | obs_upload_status |
|------|-------------|-------|---------|------------------|
| raw_img | `_handle_raw_img` | S1∥ | DataDownloader / ObsManager | ✅ 有 |
| label | `_handle_label` | S1∥ | ObsManager | ✅ 有 |
| pkl | `_handle_pkl` | S1∥ | ObsManager | ✅ 有 |
| video | `_handle_video` | S2串 | VideoGenerator | ✅ 有 |
| prompt | `_handle_prompt` | S1∥ | 动态 processor import | ✅ 有 |
| inference | `_handle_inference` | S3串 | LLMInference | ❌ 无（仅 result_paths） |

### 3.2 6 通道 handler 统一模式

每个 handler 遵循相同的 4 步模式：

```
1. 版本=-1 检查 → update_channel_status("skipped") + return
2. 通道 status 幂等检查 → task.get("{channel}_status") == "completed" → return
3. Dedup 查询（prompt 无 dedup）→ 复制路径 + update_channel_status("completed")
4. 执行生产 → running → 业务逻辑 → completed（含路径字段）/ failed
```

### 3.3 raw_img 通道

- **版本=-1**：跳过
- **缓存检查**：`_is_cached()` 检查本地缓存目录是否已存在
- **Dedup**：`try_claim_as_producer`，key 格式 `raw_img::{autosence_id}`
- **业务**：`DataDownloader.download_autoscenes()` 纯 ObsManager 管道下载
- **详细**：[[DataDownloader 数据下载器]]

### 3.4 label 通道

- **版本=-1**：跳过
- **Dedup**：key 格式 `label::{autosence_id}::{label_version}`
- **业务**：ObsManager 下载标签文件

### 3.5 pkl 通道

- **版本=-1**：跳过
- **Dedup**：key 格式 `pkl::{autosence_id}::{pkl_version}`
- **业务**：ObsManager 下载 pkl 文件

### 3.6 video 通道

- **依赖**：raw_img/label/pkl 必须先完成（Stage1 → Stage2 串行保证）
- **业务**：`VideoGenerator.gen_video()`，支持单摄/多摄拼接
- **时间戳模式**：`absolute_slice_start/end`（绝对时间戳优先）> 相对偏移 fallback
- **黑帧修复**：整路缺失抛 ValueError，单帧缺失向前搜索复制，帧数补齐
- **详细**：[[VideoGenerator 视频生成器]]、[[LLM Tools 开发规范与设计决策]] §5

### 3.7 prompt 通道

- **版本=-1**：跳过
- **无 Dedup**：prompt 通道不做去重锁
- **动态 processor import**：通过 `t_llm_version_config` 的 `processor` 字段（格式 `module.path:func_name`）动态导入处理器函数
- **业务**：生成 prompt 文本

### 3.8 inference 通道

- **依赖**：video 必须先完成（Stage2 → Stage3 串行保证）
- **Dedup**：key 格式 `inference::{autosence_id}::{data_version}::{video_config_version}::{model_version}::{prompt_version}`
- **业务**：`LLMInference.infer_single()` → 视频路径 → base64编码 → 消息构建 → API调用 → 结果解析
- **Fallback**：`run_inference_fallback()` 主推理失败时的降级推理
- **无 OBS 上传**：inference 仅保留 `result_paths`（JSONB），不上传 OBS
- **详细**：[[LLMInference LLM推理编排器]]

---

## 4. 去重锁体系

详见 [[Dedup去重锁完整设计]]、[[DedupLockManager 去重锁管理器]]、[[t_channel_dedup_lock 表]]。

### 4.1 核心运转流程

```
Producer:
  try_claim_as_producer(dedup_key, task_id, holder_id)
    → INSERT ON CONFLICT DO NOTHING (原子抢占)
      ├─ 抢占成功 → 执行生产 → complete_and_push(dedup_key, result_data)
      │                              → UPDATE status='completed', result_data=...
      │                              → 推送所有等待 Consumer (apply_result_data_to_task)
      └─ 抢占失败
           ├─ existing.status == completed → 结果复用 (apply_result_data_to_task)
           └─ existing.status == running   → Consumer 等待
           └─ existing.status == failed    → DELETE 旧锁 + INSERT 新锁 → 重试
```

### 4.2 dedup_key 构建规则

| 通道 | 格式 | 示例 |
|------|------|------|
| raw_img | `raw_img::{autosence_id}` | `raw_img::12345` |
| label | `label::{autosence_id}::{label_version}` | `label::12345::v2.1` |
| pkl | `pkl::{autosence_id}::{pkl_version}` | `pkl::12345::v3.0` |
| video | `video::{autosence_id}::{data_version}::{video_config_version}::{label_version}::{pkl_version}` | `video::12345::d1::vc2::lv3::pv4` |
| inference | `inference::{autosence_id}::{data_version}::{video_config_version}::{model_version}::{prompt_version}` | `inference::12345::d1::vc2::mv3::pv4` |

> prompt 通道无 dedup 锁。

### 4.3 三层锁治理

| 层级                | 触发           | 操作                                 | 精度                   |
| ----------------- | ------------ | ---------------------------------- | -------------------- |
| Graceful Shutdown | SIGTERM 信号   | `release_all_by_holder(holder_id)` | 精准：仅释放本进程锁           |
| 启动时孤儿锁扫描          | 进程启动         | `scan_orphan_locks()`              | 按进程：检测 holder 进程是否存活 |
| Watchdog 周期检测     | 定时 (默认30min) | 超时锁清理 + 孤儿锁清理                      | 全局扫描                 |

**holder_id 格式**：`{hostname}:{pid}:{timestamp}`，支持精准释放与孤儿锁识别。

### 4.4 回退 API 锁处理

| 操作 | 锁处理 | 通道重置 | 产物路径 |
|------|--------|---------|---------|
| retry | 释放关联锁 + 重置卡住通道 | 重置为 pending | **保留** |
| reset | 释放关联锁 + 重置 | 全部重置为 pending | **清除** |
| running/completed 通道 | 跳过 | 不处理 | 不处理 |

---

## 5. 数据表结构

### 5.1 t_llm_task（核心任务表）

详见 [[t_llm_task 表]]。

**列分组**：
- **主键/业务键**：id (UUID), task_name, autosence_id
- **版本配置**：data_version, label_version, pkl_version, video_config_version, prompt_version, model_version
- **raw_img 通道**：raw_img_status, raw_img_download_path, raw_img_obs_path, raw_img_obs_upload_status
- **label 通道**：label_status, label_download_path, label_obs_path, label_obs_upload_status
- **pkl 通道**：pkl_status, pkl_download_path, pkl_obs_path, pkl_obs_upload_status
- **video 通道**：video_status, video_local_path, video_obs_path, video_obs_upload_status
- **prompt 通道**：prompt_status, prompt_path, prompt_text, prompt_obs_path, prompt_obs_upload_status
- **inference 通道**：inference_status, result_paths (JSONB)
- **任务级**：status (派生), error_message, error_step, slice_start, slice_end, priority, attempt_count, started_at, completed_at, created_at, updated_at
- **软删除**：is_deleted

### 5.2 t_channel_dedup_lock（去重锁表）

详见 [[t_channel_dedup_lock 表]]。

**列**：id, dedup_key (UNIQUE), channel, producer_task_id, status, holder_id, result_data (JSONB), created_at, completed_at

**4 索引**：UNIQUE(dedup_key) + idx_dedup_lock_stale + idx_dedup_lock_holder_orphan + idx_dedup_lock_holder_id

### 5.3 t_llm_version_config（版本配置表）

详见 [[t_llm_version_config 表]]。

**列**：version, channel, config (JSONB), processor, processor_params (JSONB)

---

## 6. OBS 上传架构

### 6.1 上传判定

`_should_upload_obs(task, channel)` 读取各通道的 `obs_upload_status` 列判定是否需要上传。

### 6.2 上传状态流转

```
pending → uploading → completed
                    → failed
skipped (创建时即跳过)
```

### 6.3 通道覆盖

- raw_img/label/pkl/video/prompt：有独立 `obs_upload_status` 列
- inference：**无 OBS 上传逻辑**（仅保留 result_paths）
- `TaskCreator` 创建时自动填充 4 通道（raw_img/label/pkl/video）的 obs_upload_status
- prompt_obs_upload_status 在 prompt 通道执行时由 `_should_upload_obs` 按列读取

### 6.4 上传执行

`_upload_to_obs(local_path, task, channel, repo, config)` 状态流转：pending → uploading → completed/failed

---

## 7. 条件控制逻辑

### 7.1 版本=-1 跳过

raw_img/label/pkl/prompt 通道在 `data_version/label_version/pkl_version/prompt_version == -1` 时跳过，写入 `skipped`。

### 7.2 通道幂等

已 `completed` 的通道不重复写入，直接 return。

### 7.3 Dedup 结果复用

`try_claim_as_producer` 返回 `claimed=False` 且 `existing.status == completed` 时，调用 `apply_result_data_to_task` 复用结果，写入 `completed`。

### 7.4 时间戳双模式

VideoGenerator 帧过滤支持两种模式：
- **绝对时间戳模式**：`absolute_slice_start/end` 非空时，直接用绝对范围过滤
- **相对偏移模式**：否则以第一张图片时间戳为锚点

VideoProduction 中 `_resolve_slice_timestamps` 通过 ClipService 批量查询将相对偏移转为绝对时间戳。

### 7.5 动态 processor import

prompt 通道通过 `t_llm_version_config.processor`（格式 `module.path:func_name`）动态导入处理器函数。

### 7.6 inference fallback

主推理失败时调用 `run_inference_fallback()` 降级推理。

---

## 8. 边界条件处理

### 8.1 复合视频黑帧

- **整路缺失**：`_gen_composite_video` 抛出 `ValueError`（不静默贴黑帧）
- **单帧缺失**：向前搜索最近非 None 帧复制，找不到则贴黑帧
- **帧数补齐**：较短帧序列通过复制最后一个有效帧补齐到 max_frames

### 8.2 帧丢失容忍

`_filter_img_in_slice` 的 `frame_loss_threshold=0.3`（允许最多 30% 帧丢失），帧数不足返回空字典。

### 8.3 视频已存在跳过

VideoGenerator 检测视频文件已存在时直接返回成功，跳过生成。

### 8.4 缓存命中

DataDownloader `_is_cached()` 检查本地缓存目录已存在且非空时跳过下载。

### 8.5 元数据查询重试

DataDownloader `_resolve_obs_path` 元数据查询最多 3 次，间隔 5 秒。

### 8.6 软删除

`is_deleted` 字段控制逻辑删除，所有业务查询默认 `WHERE is_deleted = FALSE`，回收站查询 `WHERE is_deleted = TRUE`。

---

## 9. 异常处理流程

### 9.1 异常体系

详见 [[LLMBaseError 异常体系]]。

```
LLMBaseError (base)
├── LLMConfigError  — 配置缺失/无效（base_url/api_key 为空）
└── LLMAPIError     — API 调用失败（含 status_code + response_body）
```

### 9.2 通道级异常

通道 handler 异常 → `update_task_status("failed", error_step=channel)` + return，不继续后续通道。

### 9.3 Dedup 锁异常

| 场景 | 后果 | 兜底 |
|------|------|------|
| `kill -9` | 锁残留，holder_id 存在但进程已死 | 启动时孤儿锁扫描 + Watchdog 兜底 |
| Producer 失败 | 锁→failed 状态 | Consumer 下轮重试（claimed=True） |
| 超时 30min | 锁卡在 running | Watchdog 清理 + Consumer 重置 pending |
| 并发抢占 | 多 Worker 同时 claim | UNIQUE 约束保证原子性，仅一人成功 |

### 9.4 LLM 推理异常

- 配置缺失 → `LLMConfigError`（初始化阶段抛出）
- API 调用失败 → `LLMAPIError`（含 status_code + response_body）
- 主推理失败 → `run_inference_fallback()` 降级推理

### 9.5 视频生成异常

- 整路缺失 → `ValueError`（不静默贴黑帧）
- 图片读取异常 → 单帧缺失处理逻辑

---

## 10. 调度入口与 CLI

详见 [[TaskWorker+TaskSchedulerApp 调度入口]]。

### 10.1 TaskSchedulerApp CLI

```bash
python -m src.llm.scheduler --daemon --poll-interval 30 --limit 10
```

| 参数 | 说明 |
|------|------|
| `--daemon` | 持续轮询模式（默认 once） |
| `--once` | 单次执行后退出 |
| `--poll-interval` | 轮询间隔（秒），默认 30 |
| `--limit` | 单次拉取任务数，默认 10 |

### 10.2 运行模式

- **run_once()**：`fetch_pending_tasks(limit)` → 遍历 `process_task()` → 退出
- **run_daemon()**：循环 `fetch_pending_tasks(limit)` → 遍历 `process_task()` → sleep → 继续

### 10.3 任务拉取与抢占

`claim_task(task_id)` 乐观锁：`UPDATE WHERE status='pending' → 'running'`

---

## 11. 关联组件索引

### 调度层
- [[TaskWorker+TaskSchedulerApp 调度入口]] — 调度入口
- [[TaskExecutor 任务生产执行器]] — 3 阶段 Pipeline + 6 通道 handler
- [[TaskRepository 任务DB读写封装层]] — SQL 封装 + `_sync_task_status()`
- [[TaskCreator 任务创建器]] — JSON/JSONL → INSERT
- [[TaskQueryService 任务聚合查询]] — 概览/进度/吞吐统计

### 去重锁体系
- [[DedupLockManager 去重锁管理器]] — 锁管理核心逻辑
- [[DedupWatchdog 看门狗]] — 超时锁 + 孤儿锁清理
- [[Dedup去重锁完整设计]] — 锁体系全景设计

### 业务模块
- [[DataDownloader 数据下载器]] — ObsManager 下载管道
- [[VideoProduction 视频生产编排器]] — 视频生产 5 步编排
- [[VideoGenerator 视频生成器]] — 视频生成核心逻辑
- [[LLMInference LLM推理编排器]] — LLM 推理 4 步编排
- [[DatasetFormatter 数据集格式化器]] — ShareGPT/Qwen 格式化

### 数据模型
- [[ExchangeRecord 交换记录模型]] — 端到端闭环数据载体
- [[VideoConfig 视频配置模型]] — VideoConfig/VideoLayout/VideoTask

### 数据表
- [[t_llm_task 表]] — 核心任务表
- [[t_channel_dedup_lock 表]] — 去重锁表
- [[t_llm_version_config 表]] — 版本配置表

### 基础设施
- [[TimingCollector 时延收集器]] — 步骤级时延记录
- [[LLMBaseError 异常体系]] — LLM 域三级异常

### 规范与决策
- [[LLM Tools 开发规范与设计决策]] — 最高优先级规范
- [[任务级vs通道级status架构设计]] — status 架构核心决策
- [[LLM Tools 配置映射]] — application.yaml 字段映射
- [[LLM Tools 关键算法]] — composite/时间戳/分位数

### 架构变迁
- [[src_llm 归一合并重构记录]] — 四模块合并为 src/llm/ 的映射

### 前端交互
- [[TaskView交互流程详解]] — 任务管理前端交互
<!-- ORIGINAL_END -->
