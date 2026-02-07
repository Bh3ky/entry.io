"""Session schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class SessionCreate(BaseModel):
    """Create payload for class sessions."""

    class_id: uuid.UUID
    title: str = Field(min_length=3, max_length=255)
    description: str | None = None
    starts_at: datetime
    ends_at: datetime


class SessionUpdate(BaseModel):
    """Update payload for sessions."""

    title: str | None = Field(default=None, min_length=3, max_length=255)
    description: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None


class SessionRead(ORMModel):
    """Session response schema."""

    id: uuid.UUID
    class_id: uuid.UUID
    title: str
    description: str | None
    starts_at: datetime
    ends_at: datetime
    created_by_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
