"""Configuration loading with environment expansion and typed accessors."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from src.config.settings import ApiSettings, AppSettings, PostgresSettings

_ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-(.*?))?\}")


class ConfigError(RuntimeError):
    """Raised when the runtime configuration cannot be loaded or parsed."""


class ConfigManager:
    """Load application config once and expose typed settings to modules.

    The loader intentionally supports a tiny YAML subset used by this project so
    the config module can run before PyYAML is available in a fresh environment.
    """

    def __init__(self, config_path: str | Path | None = None) -> None:
        path = config_path or os.getenv("AI_KB_CONFIG", "config/application.yaml")
        self.config_path = Path(path)
        self._data = self._load(self.config_path)

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    @property
    def app(self) -> AppSettings:
        return AppSettings.from_mapping(self.get("app", {}))

    @property
    def api(self) -> ApiSettings:
        return ApiSettings.from_mapping(self.get("api", {}))

    @property
    def default_database_name(self) -> str:
        return str(self.get("database.default", "primary"))

    def get_postgres_settings(self, name: str | None = None) -> PostgresSettings:
        db_name = name or self.default_database_name
        data = self.get(f"database.postgresql.{db_name}")
        if not isinstance(data, dict):
            raise ConfigError(f"PostgreSQL config not found: database.postgresql.{db_name}")
        return PostgresSettings.from_mapping(db_name, data)

    def iter_postgres_settings(self) -> dict[str, PostgresSettings]:
        entries = self.get("database.postgresql", {})
        if not isinstance(entries, dict):
            return {}
        return {
            str(name): PostgresSettings.from_mapping(str(name), value)
            for name, value in entries.items()
            if isinstance(value, dict)
        }

    def get(self, path: str, default: Any = None) -> Any:
        node: Any = self._data
        for part in path.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def require(self, path: str) -> Any:
        value = self.get(path)
        if value is None:
            raise ConfigError(f"Missing required config value: {path}")
        return value

    @classmethod
    def _load(cls, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise ConfigError(f"Config file not found: {path}")
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".json":
            return json.loads(cls._expand_env(text))
        if path.suffix.lower() in {".yaml", ".yml"}:
            return cls._parse_simple_yaml(text)
        raise ConfigError(f"Unsupported config format: {path.suffix}")

    @classmethod
    def _parse_simple_yaml(cls, text: str) -> dict[str, Any]:
        root: dict[str, Any] = {}
        stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

        for line_number, raw_line in enumerate(text.splitlines(), start=1):
            line = raw_line.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            indent = len(raw_line) - len(raw_line.lstrip(" "))
            if ":" not in line:
                raise ConfigError(f"Invalid config line {line_number}: {raw_line}")

            key, raw_value = line.strip().split(":", 1)
            key = key.strip()
            raw_value = raw_value.strip()

            while stack and indent <= stack[-1][0]:
                stack.pop()
            if not stack:
                raise ConfigError(f"Invalid indentation at line {line_number}: {raw_line}")

            parent = stack[-1][1]
            if raw_value == "":
                child: dict[str, Any] = {}
                parent[key] = child
                stack.append((indent, child))
            else:
                parent[key] = cls._parse_scalar(raw_value)

        return root

    @classmethod
    def _parse_scalar(cls, value: str) -> Any:
        value = cls._expand_env(value.strip())
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if not inner:
                return []
            return [cls._parse_scalar(item.strip()) for item in inner.split(",")]
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            return cls._expand_env(value[1:-1])

        lowered = value.lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        if lowered in {"null", "none", "~"}:
            return None
        try:
            return int(value)
        except ValueError:
            return value

    @staticmethod
    def _expand_env(value: str) -> str:
        def replace(match: re.Match[str]) -> str:
            name = match.group(1)
            default = match.group(2) or ""
            return os.getenv(name, default)

        return _ENV_PATTERN.sub(replace, value)


_GLOBAL_CONFIG: ConfigManager | None = None


def get_global_config() -> ConfigManager:
    global _GLOBAL_CONFIG
    if _GLOBAL_CONFIG is None:
        _GLOBAL_CONFIG = ConfigManager()
    return _GLOBAL_CONFIG


def reset_global_config() -> None:
    global _GLOBAL_CONFIG
    _GLOBAL_CONFIG = None
