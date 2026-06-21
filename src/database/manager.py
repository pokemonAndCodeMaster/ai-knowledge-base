"""Named database connectors assembled from runtime configuration."""

from __future__ import annotations

from src.config import ConfigManager, get_global_config
from src.database.postgresql import PostgresConnector, PostgresHealth


class DatabaseManager:
    """Registry for shared database connectors.

    Business modules should ask this manager for a named connector instead of
    constructing pools directly. This keeps connection policy centralized.
    """

    def __init__(self, config: ConfigManager) -> None:
        self.config = config
        self._postgres: dict[str, PostgresConnector] = {
            name: PostgresConnector(settings)
            for name, settings in config.iter_postgres_settings().items()
        }

    def postgres(self, name: str | None = None) -> PostgresConnector:
        db_name = name or self.config.default_database_name
        if db_name not in self._postgres:
            self._postgres[db_name] = PostgresConnector(self.config.get_postgres_settings(db_name))
        return self._postgres[db_name]

    def health_check(self) -> dict[str, PostgresHealth]:
        return {name: connector.health_check() for name, connector in self._postgres.items()}

    def close(self) -> None:
        for connector in self._postgres.values():
            connector.close()


_GLOBAL_DATABASE_MANAGER: DatabaseManager | None = None


def get_global_database_manager() -> DatabaseManager:
    global _GLOBAL_DATABASE_MANAGER
    if _GLOBAL_DATABASE_MANAGER is None:
        _GLOBAL_DATABASE_MANAGER = DatabaseManager(get_global_config())
    return _GLOBAL_DATABASE_MANAGER


def reset_global_database_manager() -> None:
    global _GLOBAL_DATABASE_MANAGER
    if _GLOBAL_DATABASE_MANAGER is not None:
        _GLOBAL_DATABASE_MANAGER.close()
    _GLOBAL_DATABASE_MANAGER = None
