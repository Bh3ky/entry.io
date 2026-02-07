"""Enrollment endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead
from app.services.enrollment_service import EnrollmentService

router = APIRouter(prefix="/enrollment", tags=["enrollment"])


@router.post("", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
async def enroll_in_class(
    payload: EnrollmentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> EnrollmentRead:
    """Enroll current user in a class."""

    service = EnrollmentService(db)
    try:
        enrollment = await service.enroll(user_id=current_user.id, class_id=payload.class_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return EnrollmentRead.model_validate(enrollment)


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unenroll_from_class(
    class_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Unenroll current user from class."""

    service = EnrollmentService(db)
    try:
        await service.unenroll(user_id=current_user.id, class_id=class_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("", response_model=list[EnrollmentRead])
async def list_enrollments(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    class_id: uuid.UUID | None = Query(default=None),
) -> list[EnrollmentRead]:
    """List enrollments for current user, or by class for lead/admin."""

    service = EnrollmentService(db)
    if class_id is not None:
        if current_user.role not in {UserRole.LEAD, UserRole.ADMIN}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only lead/admin can list enrollments by class",
            )
        enrollments = await service.list_for_class(class_id)
    else:
        enrollments = await service.list_for_user(current_user.id)

    return [EnrollmentRead.model_validate(enrollment) for enrollment in enrollments]
