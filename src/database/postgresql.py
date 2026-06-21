"""PostgreSQL connector with lazy pooling and small query helpers."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator, Sequence

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

from src.config.settings import PostgresSettings


@dataclass(frozen=True)
class PostgresHealth:
    name: str
    ok: bool
    message: str


class PostgresConnector:
    """Owns one named PostgreSQL connection pool.

    Pool creation is lazy. Importing this module, constructing the connector, or
    starting FastAPI does not open a database connection until the first query.
    """

    def __init__(self, settings: PostgresSettings) -> None:
        self.settings = settings
        self._pool: SimpleConnectionPool | None = None

    @property
    def name(self) -> str:
        return self.settings.name

    def connect(self) -> SimpleConnectionPool:
        if self._pool is None:
            self._pool = SimpleConnectionPool(
                minconn=self.settings.min_connections,
                maxconn=self.settings.max_connections,
                cursor_factory=RealDictCursor,
                **self.settings.connection_kwargs(),
            )
        return self._pool

    @contextmanager
    def connection(self) -> Iterator[Any]:
        pool = self.connect()
        conn = pool.getconn()
        try:
            yield conn
        finally:
            pool.putconn(conn)

    def fetch_all(self, sql: str, params: Sequence[Any] | dict[str, Any] | None = None) -> list[dict[str, Any]]:
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return [dict(row) for row in cursor.fetchall()]

    def fetch_one(self, sql: str, params: Sequence[Any] | dict[str, Any] | None = None) -> dict[str, Any] | None:
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                row = cursor.fetchone()
                return dict(row) if row is not None else None

    def execute(self, sql: str, params: Sequence[Any] | dict[str, Any] | None = None) -> int:
        with self.connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    affected = cursor.rowcount
                conn.commit()
                return affected
            except Exception:
                conn.rollback()
                raise

    def health_check(self) -> PostgresHealth:
        try:
            row = self.fetch_one("SELECT 1 AS ok")
        except psycopg2.Error as exc:
            return PostgresHealth(name=self.name, ok=False, message=str(exc))
        except Exception as exc:
            return PostgresHealth(name=self.name, ok=False, message=str(exc))
        if row and row.get("ok") == 1:
            return PostgresHealth(name=self.name, ok=True, message="ok")
        return PostgresHealth(name=self.name, ok=False, message="unexpected health check response")

    def close(self) -> None:
        if self._pool is not None:
            self._pool.closeall()
            self._pool = None
