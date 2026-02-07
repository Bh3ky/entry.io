"""User management endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def get_my_profile(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserRead:
    """Return profile for current user."""

    return UserRead.model_validate(current_user)


@router.get("", response_model=list[UserRead])
async def list_users(
    _: Annotated[User, Depends(require_roles(UserRole.ADMIN))],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[UserRead]:
    """List all users (admin only)."""

    users = await AuthService(db).user_repo.list_users()
    return [UserRead.model_validate(user) for user in users]
