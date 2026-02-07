"""Class schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class ClassCreate(BaseModel):
    """Create payload for learning classes."""

    title: str = Field(min_length=3, max_length=255)
    description: str | None = None
    is_published: bool = True


class ClassUpdate(BaseModel):
    """Partial update payload for classes."""

    title: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = None
    is_published: bool | None = None


class ClassRead(ORMModel):
    """Class response schema."""

    id: uuid.UUID
    title: str
    description: str | None
    is_published: bool
    created_by_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
