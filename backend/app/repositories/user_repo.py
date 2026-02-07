"""Repository for user persistence operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole


class UserRepository:
    """Database operations for user entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Fetch a user by primary key."""

        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by email address."""

        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_users(self) -> list[User]:
        """Return all users ordered by creation date descending."""

        statement = select(User).order_by(User.created_at.desc())
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(
        self,
        email: str,
        hashed_password: str,
        full_name: str | None,
        role: UserRole,
    ) -> User:
        """Persist a new user record."""

        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
