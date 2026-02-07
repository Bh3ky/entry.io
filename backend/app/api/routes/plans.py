"""Quarterly planning endpoints."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.common import MessageResponse
from app.schemas.plan import PlanCreate, PlanRead, PlanUpdate
from app.services.plan_service import PlanService

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("", response_model=PlanRead, status_code=status.HTTP_201_CREATED)
async def create_plan(
    payload: PlanCreate,
    current_user: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PlanRead:
    """Create quarterly plan."""

    plan = await PlanService(db).create_plan(
        quarter=payload.quarter,
        objectives=payload.objectives,
        created_by_id=current_user.id,
    )
    return PlanRead.model_validate(plan)


@router.get("", response_model=list[PlanRead])
async def list_plans(
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PlanRead]:
    """List quarterly plans."""

    plans = await PlanService(db).list_plans()
    return [PlanRead.model_validate(plan) for plan in plans]


@router.patch("/{plan_id}", response_model=PlanRead)
async def update_plan(
    plan_id: uuid.UUID,
    payload: PlanUpdate,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PlanRead:
    """Update quarterly plan."""

    service = PlanService(db)
    try:
        plan = await service.update_plan(plan_id, payload.model_dump(exclude_none=True))
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return PlanRead.model_validate(plan)


@router.get("/{plan_id}/export")
async def export_plan(
    plan_id: uuid.UUID,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, object]:
    """Export quarterly plan as JSON."""

    service = PlanService(db)
    try:
        return await service.export_plan(plan_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{plan_id}", response_model=MessageResponse)
async def delete_plan(
    plan_id: uuid.UUID,
    _: Annotated[User, Depends(require_roles(UserRole.LEAD, UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MessageResponse:
    """Delete quarterly plan."""

    service = PlanService(db)
    try:
        await service.delete_plan(plan_id)
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return MessageResponse(message="Plan deleted")
