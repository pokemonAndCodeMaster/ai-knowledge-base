import os
import tempfile
import unittest
from pathlib import Path

from src.config import ConfigManager
from src.database import DatabaseManager


class ConfigDatabaseTest(unittest.TestCase):
    def test_config_manager_loads_application_yaml(self) -> None:
        config = ConfigManager("config/application.yaml")

        self.assertEqual(config.app.name, "ai-knowledge-base")
        self.assertEqual(config.api.version, "0.1.0")
        self.assertEqual(config.default_database_name, "primary")

    def test_environment_expansion_and_postgres_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "application.yaml"
            path.write_text(
                "\n".join(
                    [
                        "database:",
                        "  default: \"primary\"",
                        "  postgresql:",
                        "    primary:",
                        "      host: \"${TEST_PG_HOST:-localhost}\"",
                        "      port: \"${TEST_PG_PORT:-5432}\"",
                        "      database: \"demo\"",
                        "      user: \"demo_user\"",
                    ]
                ),
                encoding="utf-8",
            )

            old_host = os.environ.get("TEST_PG_HOST")
            os.environ["TEST_PG_HOST"] = "db.internal"
            try:
                config = ConfigManager(path)
                settings = config.get_postgres_settings()
            finally:
                if old_host is None:
                    os.environ.pop("TEST_PG_HOST", None)
                else:
                    os.environ["TEST_PG_HOST"] = old_host

        self.assertEqual(settings.host, "db.internal")
        self.assertEqual(settings.port, 5432)
        self.assertEqual(settings.connection_kwargs()["dbname"], "demo")

    def test_database_manager_does_not_connect_during_construction(self) -> None:
        config = ConfigManager("config/application.yaml")
        manager = DatabaseManager(config)
        connector = manager.postgres()

        self.assertEqual(connector.name, "primary")
        self.assertIsNone(connector._pool)


if __name__ == "__main__":
    unittest.main()
