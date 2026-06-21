"""Typed settings shared by API, database, and future service modules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def _as_int(value: Any, default: int) -> int:
    if value in (None, ""):
        return default
    return int(value)


@dataclass(frozen=True)
class AppSettings:
    name: str = "ai-knowledge-base"
    environment: str = "development"
    debug: bool = True

    @classmethod
    def from_mapping(cls, data: dict[str, Any] | None) -> "AppSettings":
        data = data or {}
        return cls(
            name=str(data.get("name", cls.name)),
            environment=str(data.get("environment", cls.environment)),
            debug=_as_bool(data.get("debug"), cls.debug),
        )


@dataclass(frozen=True)
class ApiSettings:
    title: str = "AI Knowledge Base API"
    version: str = "0.1.0"
    allow_origins: list[str] = field(default_factory=list)
    static_frontend_path: str = "src/frontend/dist"

    @classmethod
    def from_mapping(cls, data: dict[str, Any] | None) -> "ApiSettings":
        data = data or {}
        cors = data.get("cors") or {}
        origins = cors.get("allow_origins") or []
        return cls(
            title=str(data.get("title", cls.title)),
            version=str(data.get("version", cls.version)),
            allow_origins=[str(origin) for origin in origins],
            static_frontend_path=str(data.get("static_frontend_path", cls.static_frontend_path)),
        )


@dataclass(frozen=True)
class PostgresSettings:
    name: str
    host: str
    port: int
    database: str
    user: str
    password: str = ""
    min_connections: int = 1
    max_connections: int = 5
    connect_timeout: int = 5
    sslmode: str = "prefer"
    application_name: str = "ai-knowledge-base"

    @classmethod
    def from_mapping(cls, name: str, data: dict[str, Any]) -> "PostgresSettings":
        return cls(
            name=name,
            host=str(data.get("host", "localhost")),
            port=_as_int(data.get("port"), 5432),
            database=str(data.get("database", "postgres")),
            user=str(data.get("user", "postgres")),
            password=str(data.get("password", "")),
            min_connections=_as_int(data.get("min_connections"), 1),
            max_connections=_as_int(data.get("max_connections"), 5),
            connect_timeout=_as_int(data.get("connect_timeout"), 5),
            sslmode=str(data.get("sslmode", "prefer")),
            application_name=str(data.get("application_name", "ai-knowledge-base")),
        )

    def connection_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "host": self.host,
            "port": self.port,
            "dbname": self.database,
            "user": self.user,
            "connect_timeout": self.connect_timeout,
            "application_name": self.application_name,
        }
        if self.password:
            kwargs["password"] = self.password
        if self.sslmode:
            kwargs["sslmode"] = self.sslmode
        return kwargs
