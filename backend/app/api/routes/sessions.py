"""Session management endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.session import SessionCreate, SessionRead, SessionUpdate
from app.services.session_service import SessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: SessionCreate,
    current_user: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SessionRead:
    """Create session under class (lead/admin only)."""

    service = SessionService(db)
    try:
        session = await service.create_session(
            class_id=payload.class_id,
            title=payload.title,
            description=payload.description,
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
            created_by_id=current_user.id,
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return SessionRead.model_validate(session)


@router.get("", response_model=list[SessionRead])
async def list_sessions(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    class_id: uuid.UUID | None = Query(default=None),
) -> list[SessionRead]:
    """List sessions with optional class filter."""

    sessions = await SessionService(db).list_sessions(class_id=class_id)
    return [SessionRead.model_validate(session) for session in sessions]


@router.get("/{session_id}", response_model=SessionRead)
async def get_session(
    session_id: uuid.UUID,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SessionRead:
    """Get one session by id."""

    service = SessionService(db)
    try:
        session = await service.get_session(session_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return SessionRead.model_validate(session)


@router.patch("/{session_id}", response_model=SessionRead)
async def update_session(
    session_id: uuid.UUID,
    payload: SessionUpdate,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SessionRead:
    """Update session details (lead/admin only)."""

    service = SessionService(db)
    try:
        session = await service.update_session(
            session_id=session_id,
            updates=payload.model_dump(exclude_none=True),
        )
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return SessionRead.model_validate(session)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: uuid.UUID,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Delete session (lead/admin only)."""

    service = SessionService(db)
    try:
        await service.delete_session(session_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
