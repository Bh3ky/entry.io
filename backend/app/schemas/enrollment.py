"""Enrollment schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class EnrollmentCreate(BaseModel):
    """Request payload to enroll a member in a class."""

    class_id: uuid.UUID


class EnrollmentRead(ORMModel):
    """Enrollment response schema."""

    id: uuid.UUID
    user_id: uuid.UUID
    class_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
