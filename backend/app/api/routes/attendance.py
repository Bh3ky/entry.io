"""Attendance endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.attendance import AttendanceMarkRequest, AttendanceRead
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    payload: AttendanceMarkRequest,
    current_user: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AttendanceRead:
    """Mark attendance for a session user pair."""

    service = AttendanceService(db)
    try:
        record = await service.mark_attendance(
            session_id=payload.session_id,
            user_id=payload.user_id,
            marked_by_id=current_user.id,
            status=payload.status,
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return AttendanceRead.model_validate(record)


@router.get("/{session_id}", response_model=list[AttendanceRead])
async def list_attendance(
    session_id: uuid.UUID,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[AttendanceRead]:
    """List attendance records for one session."""

    service = AttendanceService(db)
    try:
        records = await service.list_for_session(session_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return [AttendanceRead.model_validate(record) for record in records]
