"""Class management endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.class_ import ClassCreate, ClassRead, ClassUpdate
from app.services.class_service import ClassService

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("", response_model=ClassRead, status_code=status.HTTP_201_CREATED)
async def create_class(
    payload: ClassCreate,
    current_user: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ClassRead:
    """Create a class (lead/admin only)."""

    service = ClassService(db)
    created = await service.create_class(
        title=payload.title,
        description=payload.description,
        is_published=payload.is_published,
        created_by_id=current_user.id,
    )
    return ClassRead.model_validate(created)


@router.get("", response_model=list[ClassRead])
async def list_classes(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ClassRead]:
    """List classes."""

    classes = await ClassService(db).list_classes()
    return [ClassRead.model_validate(class_) for class_ in classes]


@router.get("/{class_id}", response_model=ClassRead)
async def get_class(
    class_id: uuid.UUID,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ClassRead:
    """Get class by id."""

    service = ClassService(db)
    try:
        class_ = await service.get_class(class_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ClassRead.model_validate(class_)


@router.patch("/{class_id}", response_model=ClassRead)
async def update_class(
    class_id: uuid.UUID,
    payload: ClassUpdate,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ClassRead:
    """Update class details (lead/admin only)."""

    updates = payload.model_dump(exclude_none=True)
    service = ClassService(db)
    try:
        class_ = await service.update_class(class_id, updates)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ClassRead.model_validate(class_)


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    class_id: uuid.UUID,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Delete class (lead/admin only)."""

    service = ClassService(db)
    try:
        await service.delete_class(class_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
