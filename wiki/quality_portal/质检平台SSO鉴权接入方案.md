---
title: "质检平台权限与SSO接入设计"
domain: ["ai_dlc", "tooling"]
type: "synthesis"
tags: ["人工质检", "SSO", "权限", "鉴权", "模块等级", "最小权限"]
created: 2026-06-28
updated: 2026-06-28
sources: 6
status: active
related_code: ["task.md", "migrations/20260628_personnel_and_permission.sql", "src/api/deps.py"]
affects_path: ["src/api/auth.py", "src/api/deps.py", "src/frontend/src/features/manual-qc/"]
trigger_keywords: ["SSO", "权限等级", "acceptance_access", "personnel_access", "鉴权", "按钮权限"]
---

# 质检平台权限与 SSO 接入设计

← 总入口：[[质检一站式平台人工质检模块整体架构]]。人力表：[[人工质检-人力管理体系设计]]。API：[[质检平台-API契约与前端交互设计]]。

## 1. 初衷

平台包含验收分配、通过/打回、人力调组等高风险操作。只靠“知道网址”或前端隐藏按钮不够；后端必须根据登录身份决定是否允许调用。

当前尚无真实 SSO 参数，因此分两阶段：开发期 mock 身份，生产期接公司 SSO。业务 Service 和权限等级不随登录方式变化。

## 2. 权限存储

`t_portal_permission` 一人一行：

```text
employee_id
acceptance_access: NONE / VIEW / OPERATE / EXECUTE
personnel_access:  NONE / VIEW / MANAGE
is_admin
granted_by / updated_by / updated_at
```

采用模块等级而非每按钮 Boolean：模块内新增功能映射到已有等级，无需迁移；新增独立业务模块时才加一列。

## 3. 等级语义

| 模块 | 等级 | 包含能力 |
|---|---|---|
| 验收 | NONE | 无入口、无接口权限 |
| 验收 | VIEW | 查看策略、preview、统计、状态 |
| 验收 | OPERATE | 包含 VIEW；可刷新统计、执行验收分配 |
| 验收 | EXECUTE | 包含 OPERATE；可执行通过/打回 |
| 人力 | NONE | 无入口、无接口权限 |
| 人力 | VIEW | 查看人员、分组、画像 |
| 人力 | MANAGE | 包含 VIEW；新增、编辑、调组 |

等级顺序在后端常量集中维护，不用字符串字母顺序比较。

## 4. 后端鉴权流程

```text
请求 Authorization Header
  → auth.py 验证身份并得到 employee_id
  → 查询 t_portal_permission
  → is_admin 直接放行
  → require_access(module, minimum_level)
  → Router 调用 Service
```

未登录返回 401；已登录但权限不足返回 403；数据库无权限记录按 NONE 处理。

Router 通过 Depends 声明最低等级，Service 对批量高风险动作可再做操作者审计，不在前端自行判断安全。

## 5. 开发期 mock

- 配置 `auth.mode=mock` 时，从受控配置取得固定 employee_id。
- mock 默认只读；执行写操作需显式配置测试账号权限。
- 生产环境禁止启动 mock，可在应用启动时校验。
- 测试通过依赖覆盖注入身份，不读取真实 Token。

## 6. 生产 SSO

预期流程：浏览器完成公司 SSO 登录，前端携带 Token，后端验证签名、签发方、受众和过期时间，提取稳定工号映射到 employee_id。

以下均为 `[待人类补充]`：SSO 类型、Issuer、JWKS/公钥获取方式、Audience、工号 claim、Token 刷新和登出协议。在拿到真实信息前不编写假验证逻辑。

## 7. 前端行为

前端读取当前用户与权限：

- NONE 不显示模块入口；
- VIEW 显示只读页面和 preview；
- OPERATE 显示分配、刷新按钮；
- EXECUTE 显示通过/打回按钮；
- MANAGE 显示人员编辑和调组。

即便按钮隐藏，后端仍校验。前端不得把 `is_admin` 当成跳过后端鉴权的依据。

## 8. 审计

- 人员变更写 `t_personnel_op_log`。
- 快照记录 confirmed_by/executed_by。
- 记录权限授予者和修改者。
- 日志不记录 Token、密码或完整认证 Header。

## 9. 扩展边界

当出现项目级数据隔离、同模块互不包含的细粒度能力或批量角色授权时，再迁移 capability/RBAC。当前单项目、小团队和等级包含关系下，模块等级列更简单。

## 10. 测试

- NONE/VIEW/OPERATE/EXECUTE/MANAGE 的允许和拒绝矩阵。
- 前端隐藏但直接请求仍被后端拒绝。
- 无权限记录默认拒绝、is_admin 放行。
- mock 禁止在生产配置启动。
- Token 过期/签名错误测试在真实 SSO 参数确认后补充。

