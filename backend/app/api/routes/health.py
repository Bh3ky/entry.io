"""Health and info endpoints."""

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Liveness probe endpoint."""

    return {"status": "ok"}


@router.get("/info")
async def app_info() -> dict[str, str]:
    """Basic app metadata endpoint."""

    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "environment": settings.env,
        "api_prefix": settings.api_v1_prefix,
    }
