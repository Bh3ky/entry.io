"""Announcement endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.announcement import AnnouncementCreate, AnnouncementRead
from app.services.announcement_service import AnnouncementService

router = APIRouter(prefix="/announcements", tags=["announcements"])


@router.post("", response_model=AnnouncementRead, status_code=status.HTTP_201_CREATED)
async def create_announcement(
    payload: AnnouncementCreate,
    current_user: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AnnouncementRead:
    """Create announcement (lead/admin only)."""

    created = await AnnouncementService(db).create_announcement(
        title=payload.title,
        body=payload.body,
        created_by_id=current_user.id,
    )
    return AnnouncementRead.model_validate(created)


@router.get("", response_model=list[AnnouncementRead])
async def list_announcements(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[AnnouncementRead]:
    """List announcements."""

    announcements = await AnnouncementService(db).list_announcements()
    return [AnnouncementRead.model_validate(item) for item in announcements]


@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    announcement_id: uuid.UUID,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Delete announcement (lead/admin only)."""

    try:
        await AnnouncementService(db).delete_announcement(announcement_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
