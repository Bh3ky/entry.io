"""Shared pytest fixtures for API integration tests."""

import asyncio
from collections.abc import Generator
import importlib.util

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.rate_limit import rate_limiter
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import UserRole
from app.services.auth_service import AuthService

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
HAS_AIOSQLITE = importlib.util.find_spec("aiosqlite") is not None

if HAS_AIOSQLITE:
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionForTests = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
else:
    engine = None
    SessionForTests = None


async def _create_all_tables() -> None:
    if engine is None:
        return
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def _drop_all_tables() -> None:
    if engine is None:
        return
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
def prepare_test_db() -> Generator[None, None, None]:
    """Create and tear down all tables for each test."""

    if HAS_AIOSQLITE:
        asyncio.run(_create_all_tables())
    rate_limiter._events.clear()
    yield
    rate_limiter._events.clear()
    if HAS_AIOSQLITE:
        asyncio.run(_drop_all_tables())


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide test client with test database dependency override."""

    if not HAS_AIOSQLITE:
        with TestClient(app) as test_client:
            yield test_client
        return

    async def override_get_db() -> Generator[AsyncSession, None, None]:
        assert SessionForTests is not None
        async with SessionForTests() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def create_user():
    """Factory fixture creating users and bearer auth headers."""

    if not HAS_AIOSQLITE:
        pytest.skip("aiosqlite is required to run database-backed tests in this environment")

    def _create_user(
        email: str,
        role: UserRole = UserRole.MEMBER,
        password: str = "Password123!",
    ) -> dict[str, str]:
        async def run() -> dict[str, str]:
            assert SessionForTests is not None
            async with SessionForTests() as session:
                service = AuthService(session)
                await service.register(
                    email=email,
                    password=password,
                    full_name="Test User",
                    role=role,
                )
                access_token, _ = await service.authenticate(email=email, password=password)
                return {"Authorization": f"Bearer {access_token}"}

        return asyncio.run(run())

    return _create_user


@pytest.fixture
def require_db_driver() -> None:
    """Skip DB-backed tests when async sqlite driver is unavailable."""

    if not HAS_AIOSQLITE:
        pytest.skip("aiosqlite is not installed; skipping DB-backed tests")
