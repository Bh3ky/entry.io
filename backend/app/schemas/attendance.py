"""Attendance schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.attendance import AttendanceStatus
from app.schemas.common import ORMModel


class AttendanceMarkRequest(BaseModel):
    """Request payload to mark or update attendance."""

    session_id: uuid.UUID
    user_id: uuid.UUID
    status: AttendanceStatus


class AttendanceRead(ORMModel):
    """Attendance response schema."""

    id: uuid.UUID
    session_id: uuid.UUID
    user_id: uuid.UUID
    marked_by_id: uuid.UUID
    status: AttendanceStatus
    created_at: datetime
    updated_at: datetime
