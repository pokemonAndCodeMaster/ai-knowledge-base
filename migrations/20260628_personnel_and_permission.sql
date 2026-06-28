-- ============================================================
-- 质检一站式平台 -- 人力管理 & 前端权限 DDL (简化版)
-- Migration: 20260628_personnel_and_permission.sql
-- 设计原则：一人一行，所有属性平铺，枚举约束，历史变更靠 op_log
-- 说明：暂无本地实例，此文件为设计稿
-- PostgreSQL 兼容基线：10+（不使用 identity、generated column、NULLS NOT DISTINCT 等高版本语法）
-- ============================================================

BEGIN;

-- ============================================================
-- PART 1: 人员主表（3个角色合一张表）
-- ============================================================
-- role 枚举：
--   ANNOTATOR        外包标注员（FP/计件制）
--   ACCEPTOR         外包验收员（TM/固定工资）
--   INTERNAL_CHECKER 华为内部员工，用于抽检验收员质量
-- level 枚举（ANNOTATOR 有效）：
--   STANDARD  一般标注员
--   SENIOR    高阶标注员（计件单价更高）
--   N/A       验收员/内部员工填此值
-- status 枚举：
--   ACTIVE    在职
--   INACTIVE  暂停（临时不参与任务）
--   LEAVE     离职

CREATE TABLE t_personnel (
    id              SERIAL       PRIMARY KEY,
    employee_id     VARCHAR(64)  NOT NULL,           -- 工号（外包供应商工号 or 华为工号）
    name            VARCHAR(64)  NOT NULL,
    email           VARCHAR(128),
    phone           VARCHAR(32),

    -- 角色与层级
    role            VARCHAR(20)  NOT NULL,
    level           VARCHAR(16)  NOT NULL DEFAULT 'STANDARD',

    -- 供应商（INTERNAL_CHECKER 可 NULL，直接存名称无需 FK）
    supplier        VARCHAR(128),

    -- 当前项目（一人同一时刻只属于一个项目）
    project_name    VARCHAR(64)  NOT NULL,

    -- 当前所在组（组概念属于标注员，格式: "城区A组"；验收员/内部员工留空）
    current_group   VARCHAR(128) NOT NULL DEFAULT '',

    -- 财务
    unit_price      NUMERIC(10,4),                   -- FP 计件单价，仅 ANNOTATOR 有效

    -- 在职状态
    status          VARCHAR(16)  NOT NULL DEFAULT 'ACTIVE',
    join_date       DATE         NOT NULL,
    leave_date      DATE,                            -- NULL = 在职

    notes           TEXT,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(64),                     -- 最后修改人工号

    CONSTRAINT uq_personnel_employee_id     UNIQUE (employee_id),
    CONSTRAINT ck_personnel_role            CHECK  (role   IN ('ANNOTATOR','ACCEPTOR','INTERNAL_CHECKER')),
    CONSTRAINT ck_personnel_level           CHECK  (level  IN ('STANDARD','SENIOR','N/A')),
    CONSTRAINT ck_personnel_status          CHECK  (status IN ('ACTIVE','INACTIVE','LEAVE')),
    CONSTRAINT ck_personnel_project         CHECK  (BTRIM(project_name) <> ''),
    CONSTRAINT ck_personnel_level_by_role   CHECK  (
        (role = 'ANNOTATOR' AND level IN ('STANDARD','SENIOR'))
        OR
        (role IN ('ACCEPTOR','INTERNAL_CHECKER') AND level = 'N/A')
    ),
    -- 外包人员必须填供应商
    CONSTRAINT ck_supplier_required         CHECK  (role = 'INTERNAL_CHECKER' OR COALESCE(BTRIM(supplier), '') <> ''),
    -- 计件单价只对标注员有意义
    CONSTRAINT ck_unit_price_annotator_only CHECK  (unit_price IS NULL OR (role = 'ANNOTATOR' AND unit_price >= 0)),
    -- 组只对标注员有意义
    CONSTRAINT ck_group_annotator_only      CHECK  (role = 'ANNOTATOR' OR current_group = ''),
    CONSTRAINT ck_leave_date_range          CHECK  (leave_date IS NULL OR leave_date >= join_date),
    CONSTRAINT ck_leave_status_date         CHECK  (status <> 'LEAVE' OR leave_date IS NOT NULL)
);

COMMENT ON TABLE  t_personnel              IS '人力主表：外包标注员/外包验收员/华为内部抽检员，一人一行';
COMMENT ON COLUMN t_personnel.supplier     IS '供应商名称，直接存字符串；INTERNAL_CHECKER 可为 NULL';
COMMENT ON COLUMN t_personnel.project_name IS '当前所属项目；一人同一时刻只允许属于一个项目';
COMMENT ON COLUMN t_personnel.current_group IS '当前所在标注员组名；验收员/内部员工为空串';
COMMENT ON COLUMN t_personnel.unit_price   IS 'FP 计件单价，仅 ANNOTATOR 有效，NULL=待录入';

CREATE INDEX idx_personnel_role    ON t_personnel (role);
CREATE INDEX idx_personnel_status  ON t_personnel (status);
CREATE INDEX idx_personnel_group   ON t_personnel (current_group) WHERE current_group <> '';
CREATE INDEX idx_personnel_project  ON t_personnel (project_name, status, role);


-- ============================================================
-- PART 2: 人员操作记录表（审计，保留变更历史）
-- ============================================================
-- action 枚举：UPDATE / ADD / DEACTIVATE / GROUP_CHANGE / PROJECT_CHANGE

CREATE TABLE t_personnel_op_log (
    id           BIGSERIAL   PRIMARY KEY,
    operated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    operator_id  VARCHAR(64) NOT NULL,               -- 操作人工号
    personnel_id INT         NOT NULL REFERENCES t_personnel(id),
    action       VARCHAR(32) NOT NULL,               -- UPDATE / ADD / DEACTIVATE / GROUP_CHANGE 等
    changes      JSONB       NOT NULL DEFAULT '{}',  -- {"field": {"old": ..., "new": ...}}
    notes        TEXT,

    CONSTRAINT ck_op_action CHECK (action IN ('ADD','UPDATE','DEACTIVATE','GROUP_CHANGE','PROJECT_CHANGE','REACTIVATE'))
);

COMMENT ON TABLE  t_personnel_op_log       IS '人员操作记录：谁改了谁的哪个字段，保留变更历史';
COMMENT ON COLUMN t_personnel_op_log.changes IS 'JSONB {字段名: {old: 旧值, new: 新值}}';

CREATE INDEX idx_op_log_personnel ON t_personnel_op_log (personnel_id, operated_at DESC);
CREATE INDEX idx_op_log_operator  ON t_personnel_op_log (operator_id, operated_at DESC);


-- ============================================================
-- PART 3: 前端权限表（SSO 鉴权预留，一人一行，每列一个业务模块）
-- ============================================================
-- 设计原则：同一模块内使用权限等级，避免每个按钮新增一个 BOOLEAN 列。
-- 新功能归入既有等级时无需改表；只有新增独立业务模块时才新增权限列。
-- 当前支持模块：
--   验收模块：NONE / VIEW / OPERATE / EXECUTE
--   人力管理：NONE / VIEW / MANAGE
--   (未来扩展) 标注进度：view
--   (未来扩展) 大模型质检：view / operate

CREATE TABLE t_portal_permission (
    id              SERIAL      PRIMARY KEY,
    employee_id     VARCHAR(64) NOT NULL,            -- 来自公司 SSO JWT sub 字段（工号）
    name            VARCHAR(64),                     -- 冗余姓名，方便直接展示

    -- 验收模块：VIEW=只读；OPERATE=可分配；EXECUTE=可通过/打回（并包含低等级能力）
    acceptance_access       VARCHAR(16) NOT NULL DEFAULT 'NONE',

    -- 人力管理模块：VIEW=只读；MANAGE=可新增、修改和调组
    personnel_access        VARCHAR(16) NOT NULL DEFAULT 'NONE',

    -- 管理员
    is_admin                BOOLEAN NOT NULL DEFAULT FALSE,

    -- 元数据
    granted_by  VARCHAR(64),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by  VARCHAR(64),

    CONSTRAINT uq_permission_employee UNIQUE (employee_id),
    CONSTRAINT ck_acceptance_access CHECK (acceptance_access IN ('NONE','VIEW','OPERATE','EXECUTE')),
    CONSTRAINT ck_personnel_access  CHECK (personnel_access  IN ('NONE','VIEW','MANAGE'))
);

COMMENT ON TABLE  t_portal_permission             IS 'SSO鉴权权限表：一人一行，每列一个业务模块的权限等级';
COMMENT ON COLUMN t_portal_permission.employee_id IS '来自公司SSO JWT sub字段（工号），与 t_personnel.employee_id 对应但不做 FK';
COMMENT ON COLUMN t_portal_permission.is_admin    IS '超级管理员，所有权限自动为 TRUE，后端中间件短路判断';
COMMENT ON COLUMN t_portal_permission.acceptance_access IS '验收权限等级：NONE/VIEW/OPERATE/EXECUTE，等级能力由后端统一映射';
COMMENT ON COLUMN t_portal_permission.personnel_access  IS '人力权限等级：NONE/VIEW/MANAGE，等级能力由后端统一映射';

COMMIT;
