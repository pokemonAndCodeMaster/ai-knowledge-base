"""FastAPI application factory."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.routers import health
from src.manual_qc.acceptance import router as acceptance_router
from src.config import get_global_config
from src.database import reset_global_database_manager


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    reset_global_database_manager()


def create_app() -> FastAPI:
    config = get_global_config()
    app_settings = config.app
    api_settings = config.api

    app = FastAPI(title=api_settings.title, version=api_settings.version, debug=app_settings.debug, lifespan=lifespan)

    if api_settings.allow_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=api_settings.allow_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(health.router)
    app.include_router(acceptance_router.router)

    frontend_path = Path(api_settings.static_frontend_path)
    if frontend_path.exists():
        app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

    return app


app = create_app()
