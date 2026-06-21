"""Common API response schemas."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class ApiResponse(GenericModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T


class PageResult(GenericModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int


class HealthData(BaseModel):
    service: str
    environment: str
    status: str
