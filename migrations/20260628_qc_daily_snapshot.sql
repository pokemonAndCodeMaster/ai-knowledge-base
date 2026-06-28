-- ============================================================
-- 质检一站式平台 -- 综合质检日常快照表 DDL (v2，合并标注+验收)
-- Migration: 20260628_qc_daily_snapshot.sql
-- 依赖：20260628_personnel_and_permission.sql（t_personnel）
-- PostgreSQL 兼容基线：10+（不使用 generated column、NULLS NOT DISTINCT 等高版本语法）
-- ============================================================
-- 设计原则：
--   1. 一行 = 一个 (stat_date × scene_name × group_name × annotator_id) 维度组合
--   2. 同一行承载该维度下的标注进度、标注结果分布、验收分配、验收结果
--   3. 执行通过/打回的结论和执行状态也记录在同一行，无需跨表 JOIN
--   4. group_name 冗余存储（不做 FK），便于按组 GROUP BY 聚合
--   5. 每行必须绑定 annotator_id；group_name 记录该标注员在 stat_date 当天的组别
--   6. sampler 从本表计算各最小统计单元的抽样配额；真正执行时再按这些维度查询任务级中间表/Delta 表取得 clip/task_id
--   7. acceptance_allocated 等执行量以回查 Delta 任务状态后的实际结果为准，不以接口请求数量为准
-- ============================================================

BEGIN;
--
-- 场景说明（scene_name 概念）：
--   scene_name 是上游批次/任务组的抽象概念。上游送入人工质检的任务一般是
--   一批数据一个任务组，通常是同一类场景或同一批次采集/挖掘的数据。
--   scene_name 是整个质检流程管理的最小自然单位，用于：
--     - 标注任务查询和筛选
--     - 验收分配时的抽样分组
--     - 统计报表的分组维度
--     - 快照表的主要维度键
-- ============================================================

CREATE TABLE t_qc_daily_snapshot (
    id              BIGSERIAL    PRIMARY KEY,

    -- ---- 维度键 ------------------------------------------------
    stat_date       DATE         NOT NULL,
    scene_name      VARCHAR(256) NOT NULL,       -- 任务组/场景名（上游批次概念）
    group_name      VARCHAR(128) NOT NULL DEFAULT '',   -- 冗余存储标注员组名（便于 GROUP BY 聚合）
    annotator_id    INT          NOT NULL REFERENCES t_personnel(id),

    -- ---- 标注进度 -----------------------------------------------
    annotation_total        INT NOT NULL DEFAULT 0,  -- 该维度下分配的标注任务总数
    annotation_submitted    INT NOT NULL DEFAULT 0,  -- 已提交/完成标注数（标注员已完成）
    annotation_pending      INT NOT NULL DEFAULT 0,  -- 待标注数 = total - submitted

    -- ---- 标注结果分布（各选项数量）-------------------------------
    -- JSONB: {"A": 120, "B": 30, "C": 15, "D": 5}
    -- key = 选项字母，value = 该选项的标注数量
    option_annotation       JSONB NOT NULL DEFAULT '{}',

    -- ---- 验收分配情况 -------------------------------------------
    acceptance_allocated    INT NOT NULL DEFAULT 0,  -- 回查任务状态后确认已成功分配到验收员的数量
    -- 分配比例 = acceptance_allocated / annotation_submitted，可在应用层计算

    -- ---- 验收进度 -----------------------------------------------
    acceptance_submitted    INT NOT NULL DEFAULT 0,  -- 已完成验收数（验收员已判定）

    -- ---- 验收结果（Good/Bad 分层）--------------------------------
    good_allocated          INT NOT NULL DEFAULT 0,  -- 分配的 Good 类任务数
    good_passed             INT NOT NULL DEFAULT 0,  -- Good 类验收通过数
    bad_allocated           INT NOT NULL DEFAULT 0,  -- 分配的 Bad 类任务数
    bad_passed              INT NOT NULL DEFAULT 0,  -- Bad 类验收通过数

    -- ---- 各选项验收明细 ------------------------------------------
    -- JSONB: {"A": {"allocated": 100, "passed": 96},
    --         "B": {"allocated": 25,  "passed": 18},
    --         "C": {"allocated": 12,  "passed": 9}}
    -- key = 选项字母，value = {allocated: 分配数, passed: 通过数}
    option_acceptance       JSONB NOT NULL DEFAULT '{}',

    -- ---- 执行结论（通过/打回决策）--------------------------------
    -- 状态流转: NULL → PENDING（正在分析）→ PASS/REJECT（结论确认）
    conclusion              VARCHAR(16),
    -- JSONB 存储决策依据，如通过率：
    -- {"good_pass_rate": 0.96, "bad_pass_rate": 0.82, "rule_used": "RateBasedPassRule"}
    conclusion_basis        JSONB,
    confirmed_by            VARCHAR(64),   -- 确认人工号（点"确认结论"的操作人）
    confirmed_at            TIMESTAMPTZ,

    -- ---- 执行状态（真正调用 Delta API 通过/打回）------------------
    is_executed             BOOLEAN      NOT NULL DEFAULT FALSE,
    executed_by             VARCHAR(64),   -- 执行人工号
    executed_at             TIMESTAMPTZ,
    execution_note          TEXT,

    -- ---- 元数据 -------------------------------------------------
    computed_at             TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_snapshot UNIQUE (stat_date, scene_name, group_name, annotator_id),
    CONSTRAINT ck_conclusion CHECK (conclusion IN ('PENDING','PASS','REJECT') OR conclusion IS NULL),
    CONSTRAINT ck_annotation_counts_nonnegative CHECK (
        annotation_total >= 0 AND annotation_submitted >= 0 AND annotation_pending >= 0
    ),
    CONSTRAINT ck_annotation_counts_order CHECK (
        annotation_submitted <= annotation_total
        AND annotation_pending = annotation_total - annotation_submitted
    ),
    CONSTRAINT ck_acceptance_counts_nonnegative CHECK (
        acceptance_allocated >= 0 AND acceptance_submitted >= 0
        AND good_allocated >= 0 AND good_passed >= 0
        AND bad_allocated >= 0 AND bad_passed >= 0
    ),
    CONSTRAINT ck_acceptance_counts_order CHECK (
        acceptance_allocated <= annotation_submitted
        AND acceptance_submitted <= acceptance_allocated
        AND good_allocated + bad_allocated <= acceptance_allocated
        AND good_passed <= good_allocated
        AND bad_passed <= bad_allocated
        AND good_passed + bad_passed <= acceptance_submitted
    ),
    CONSTRAINT ck_execution_fields CHECK (
        is_executed = FALSE
        OR (conclusion IN ('PASS','REJECT') AND executed_by IS NOT NULL AND executed_at IS NOT NULL)
    )
);

COMMENT ON TABLE  t_qc_daily_snapshot IS '综合质检日常快照：一行=一个(日期×场景×组×人)维度组合，涵盖标注进度、验收进度和执行结论';
COMMENT ON COLUMN t_qc_daily_snapshot.stat_date         IS '统计日期（标注提交日期）';
COMMENT ON COLUMN t_qc_daily_snapshot.scene_name        IS 'scene_name: 任务组/场景名，上游批次概念，质检流程的最小自然管理单位';
COMMENT ON COLUMN t_qc_daily_snapshot.group_name        IS '记录该标注员在 stat_date 当天的组名，便于直接按历史组别聚合；非 FK，后续调组不回写历史';
COMMENT ON COLUMN t_qc_daily_snapshot.annotator_id      IS '最小统计单元对应的标注员；不允许 NULL，不在本表重复存组级汇总行';
COMMENT ON COLUMN t_qc_daily_snapshot.annotation_total  IS '该维度下分配的标注任务总数（含未完成）';
COMMENT ON COLUMN t_qc_daily_snapshot.option_annotation IS 'JSONB: {选项字母: 标注数量}，各选项的标注结果分布';
COMMENT ON COLUMN t_qc_daily_snapshot.option_acceptance IS 'JSONB: {选项字母: {allocated: N, passed: N}}，各选项的验收情况';
COMMENT ON COLUMN t_qc_daily_snapshot.conclusion        IS '通过/打回结论：NULL=未评估 PENDING=评估中 PASS=通过 REJECT=打回';
COMMENT ON COLUMN t_qc_daily_snapshot.conclusion_basis  IS 'JSONB: 决策依据（通过率、使用的规则名等）';
COMMENT ON COLUMN t_qc_daily_snapshot.is_executed       IS 'TRUE=已调用 Delta API 完成真实的通过/打回操作';
COMMENT ON COLUMN t_qc_daily_snapshot.acceptance_allocated IS '实际分配成功量：根据任务级中间表/Delta 状态回查后刷新，可与采样预期量对比发现接口部分失败';

-- 高频查询索引
CREATE INDEX idx_snapshot_date       ON t_qc_daily_snapshot (stat_date DESC);
CREATE INDEX idx_snapshot_scene      ON t_qc_daily_snapshot (scene_name, stat_date DESC);
CREATE INDEX idx_snapshot_group      ON t_qc_daily_snapshot (group_name, stat_date DESC) WHERE group_name <> '';
CREATE INDEX idx_snapshot_annotator  ON t_qc_daily_snapshot (annotator_id, stat_date DESC);
CREATE INDEX idx_snapshot_conclusion ON t_qc_daily_snapshot (conclusion, is_executed) WHERE conclusion IS NOT NULL;
-- 用于查找"已有结论但未执行"的待办行
CREATE INDEX idx_snapshot_pending_exec ON t_qc_daily_snapshot (stat_date DESC)
    WHERE conclusion IN ('PASS','REJECT') AND is_executed = FALSE;

COMMIT;
