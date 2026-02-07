"""User schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.user import UserRole
from app.schemas.common import ORMModel


class UserCreate(BaseModel):
    """Input schema for creating users in services/tests."""

    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)
    role: UserRole = UserRole.MEMBER


class UserRead(ORMModel):
    """Public user representation."""

    id: uuid.UUID
    email: str
    full_name: str | None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
