"""Announcement schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class AnnouncementCreate(BaseModel):
    """Create payload for announcements."""

    title: str = Field(min_length=3, max_length=255)
    body: str = Field(min_length=3)


class AnnouncementRead(ORMModel):
    """Announcement response schema."""

    id: uuid.UUID
    title: str
    body: str
    created_by_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
