"""Basic in-memory rate limiting helpers."""

from collections import defaultdict, deque
from collections.abc import Callable
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
    """Simple rolling-window rate limiter keyed by client + route."""

    def __init__(self) -> None:
        self._events: dict[str, deque[datetime]] = defaultdict(deque)

    def _key(self, request: Request) -> str:
        client = request.client.host if request.client else "unknown"
        return f"{client}:{request.url.path}"

    def check(self, request: Request, limit: int, window_seconds: int) -> None:
        """Raise HTTP 429 when the request exceeds the configured window."""

        key = self._key(request)
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(seconds=window_seconds)

        events = self._events[key]
        while events and events[0] < window_start:
            events.popleft()

        if len(events) >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
            )

        events.append(now)


rate_limiter = InMemoryRateLimiter()


def rate_limit(limit: int, window_seconds: int) -> Callable[[Request], None]:
    """Create a FastAPI dependency that enforces an in-memory rate limit."""

    def dependency(request: Request) -> None:
        rate_limiter.check(request, limit=limit, window_seconds=window_seconds)

    return dependency
