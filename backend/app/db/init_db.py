"""Database initialization helpers for local development."""

from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.base import Base


async def create_all_tables(engine: AsyncEngine) -> None:
    """Create all mapped tables."""

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def drop_all_tables(engine: AsyncEngine) -> None:
    """Drop all mapped tables."""

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
