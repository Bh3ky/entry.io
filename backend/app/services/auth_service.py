"""Authentication service layer."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository


class AuthError(Exception):
    """Raised when authentication fails."""


class AuthService:
    """Business logic for registration, login, and token refresh."""

    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = UserRepository(session)

    async def register(
        self,
        email: str,
        password: str,
        full_name: str | None,
        role: UserRole = UserRole.MEMBER,
    ) -> User:
        """Create a user account with hashed password."""

        existing_user = await self.user_repo.get_by_email(email=email)
        if existing_user is not None:
            raise AuthError("Email is already registered")

        hashed_password = hash_password(password)
        return await self.user_repo.create(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
        )

    async def authenticate(self, email: str, password: str) -> tuple[str, str]:
        """Validate credentials and return access+refresh tokens."""

        user = await self.user_repo.get_by_email(email=email)
        if user is None or not verify_password(password, user.hashed_password):
            raise AuthError("Invalid email or password")

        if not user.is_active:
            raise AuthError("User account is inactive")

        access_token = create_access_token(subject=str(user.id), role=user.role.value)
        refresh_token = create_refresh_token(subject=str(user.id), role=user.role.value)
        return access_token, refresh_token

    async def refresh(self, refresh_token: str) -> tuple[str, str]:
        """Create a new token pair from a valid refresh token."""

        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise AuthError("Invalid token type for refresh")

        user_id = payload.get("sub")
        role = payload.get("role")
        if not user_id or not role:
            raise AuthError("Invalid refresh token payload")

        access_token = create_access_token(subject=user_id, role=role)
        new_refresh_token = create_refresh_token(subject=user_id, role=role)
        return access_token, new_refresh_token
