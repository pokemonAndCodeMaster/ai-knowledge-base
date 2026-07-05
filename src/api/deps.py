"""FastAPI dependency providers.

Routers depend on these functions instead of importing concrete infrastructure
directly. That keeps router code thin and makes later tests simpler.
"""

from src.config import ConfigManager, get_global_config
from src.database import DatabaseManager, PostgresConnector, get_global_database_manager
from src.manual_qc.acceptance.services.query_service import AcceptanceQueryService
from src.manual_qc.acceptance.services.assignment_preview_service import AssignmentPreviewService
from src.manual_qc.repository import AcceptanceRepository


def get_config() -> ConfigManager:
    return get_global_config()


def get_database_manager() -> DatabaseManager:
    return get_global_database_manager()


def get_postgres() -> PostgresConnector:
    return get_database_manager().postgres()


def get_acceptance_query_service() -> AcceptanceQueryService:
    repository = AcceptanceRepository(get_postgres())
    return AcceptanceQueryService(repository)


def get_assignment_preview_service() -> AssignmentPreviewService:
    repository = AcceptanceRepository(get_postgres())
    return AssignmentPreviewService(repository)
