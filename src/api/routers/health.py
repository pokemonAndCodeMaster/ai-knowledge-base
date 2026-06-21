"""Health endpoints for API and infrastructure checks."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from src.api.deps import get_config, get_database_manager
from src.config import ConfigManager
from src.database import DatabaseManager

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health(config: ConfigManager = Depends(get_config)) -> dict[str, object]:
    app_settings = config.app
    return {
        "code": 0,
        "message": "success",
        "data": {
            "service": app_settings.name,
            "environment": app_settings.environment,
            "status": "ok",
        },
    }


@router.get("/health/database")
def database_health(manager: DatabaseManager = Depends(get_database_manager)) -> dict[str, object]:
    checks = manager.health_check()
    data = {
        name: {"ok": result.ok, "message": result.message}
        for name, result in checks.items()
    }
    ok = all(item["ok"] for item in data.values()) if data else True
    return {
        "code": 0 if ok else 1,
        "message": "success" if ok else "database health check failed",
        "data": data,
    }
