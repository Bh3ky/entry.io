"""Authentication request and response schemas."""

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    """Payload for new user registration."""

    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


class LoginRequest(BaseModel):
    """Payload for login credentials."""

    email: str
    password: str


class TokenResponse(BaseModel):
    """JWT tokens returned on successful auth operations."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Payload for token refresh operations."""

    refresh_token: str
