"""验收(Acceptance)内聚子包。

按职责分层：
    models.py       — 仅放模块内多个组件稳定复用的数据结构
    sampler.py      — 采样配额计算（Strategy Pattern）
    pass_rules.py   — 通过/打回规则（Strategy Pattern）
    services/       — 应用服务（编排层）
    router.py       — FastAPI 路由（HTTP 入口）

共享数据库访问和 Delta 平台调用分别位于上层 repository.py、delta_client.py。
"""
