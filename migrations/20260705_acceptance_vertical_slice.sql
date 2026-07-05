BEGIN;

CREATE TABLE IF NOT EXISTS t_qc_delivery_task (
    id                  BIGSERIAL PRIMARY KEY,
    task_code           VARCHAR(64) NOT NULL UNIQUE,
    dataset_name        VARCHAR(256) NOT NULL,
    scene_name          VARCHAR(256) NOT NULL UNIQUE,
    topic               VARCHAR(64) NOT NULL,
    priority            VARCHAR(8) NOT NULL DEFAULT 'P1',
    expected_delivery_at DATE,
    expected_quantity   INT NOT NULL DEFAULT 0,
    status              VARCHAR(32) NOT NULL DEFAULT 'ACCEPTANCE_PENDING',
    owner_employee_id   VARCHAR(64),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_delivery_priority CHECK (priority IN ('P0','P1','P2')),
    CONSTRAINT ck_delivery_quantity CHECK (expected_quantity >= 0)
);

CREATE INDEX IF NOT EXISTS idx_delivery_topic_status
    ON t_qc_delivery_task (topic, status, expected_delivery_at);

CREATE TABLE IF NOT EXISTS t_qc_operation_preview (
    preview_id          VARCHAR(64) PRIMARY KEY,
    operation_type      VARCHAR(32) NOT NULL,
    created_by          VARCHAR(64) NOT NULL,
    selection_spec      JSONB NOT NULL,
    request_payload     JSONB NOT NULL,
    result_summary      JSONB NOT NULL,
    source_version      VARCHAR(128) NOT NULL,
    status              VARCHAR(16) NOT NULL DEFAULT 'READY',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ NOT NULL,
    executed_at         TIMESTAMPTZ,
    CONSTRAINT ck_preview_status CHECK (status IN ('READY','EXPIRED','EXECUTED','INVALIDATED'))
);

CREATE INDEX IF NOT EXISTS idx_preview_owner_status
    ON t_qc_operation_preview (created_by, status, expires_at DESC);

CREATE TABLE IF NOT EXISTS t_portal_view_config (
    id                  BIGSERIAL PRIMARY KEY,
    config_key          VARCHAR(128) NOT NULL,
    module_key          VARCHAR(128) NOT NULL,
    config_type         VARCHAR(32) NOT NULL,
    owner_employee_id   VARCHAR(64),
    is_public           BOOLEAN NOT NULL DEFAULT FALSE,
    config_payload      JSONB NOT NULL,
    version             INT NOT NULL DEFAULT 1,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by          VARCHAR(64),
    CONSTRAINT uq_view_config UNIQUE (config_key, owner_employee_id),
    CONSTRAINT ck_view_config_type CHECK (config_type IN ('TABLE_VIEW','DASHBOARD_LAYOUT','DASHBOARD_CARD'))
);

COMMIT;
