"""Quarterly plan schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class PlanCreate(BaseModel):
    """Create payload for quarterly plans."""

    quarter: str = Field(min_length=4, max_length=20)
    objectives: list[dict[str, str]] = Field(default_factory=list)


class PlanUpdate(BaseModel):
    """Update payload for quarterly plans."""

    quarter: str | None = Field(default=None, min_length=4, max_length=20)
    objectives: list[dict[str, str]] | None = None


class PlanRead(ORMModel):
    """Quarterly plan response schema."""

    id: uuid.UUID
    quarter: str
    objectives: list[dict[str, str]]
    created_by_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
