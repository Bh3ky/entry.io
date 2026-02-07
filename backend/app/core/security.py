"""Security utilities for password hashing and JWT-like token handling.

This module intentionally uses only Python standard library primitives so the
project can run in constrained environments without optional crypto packages.
"""

import base64
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
import secrets
from typing import Any

from app.core.config import get_settings


class TokenDecodeError(Exception):
    """Raised when a token cannot be decoded or validated."""


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


def _sign(message: bytes, secret_key: str) -> bytes:
    return hmac.new(secret_key.encode("utf-8"), message, hashlib.sha256).digest()


def _encode_jwt(payload: dict[str, Any], secret_key: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}

    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64url_encode(
        json.dumps(payload, separators=(",", ":"), default=str).encode("utf-8")
    )

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature_b64 = _b64url_encode(_sign(signing_input, secret_key))
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def _decode_jwt(token: str, secret_key: str) -> dict[str, Any]:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise TokenDecodeError("Malformed token") from exc

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected_sig = _sign(signing_input, secret_key)
    provided_sig = _b64url_decode(signature_b64)

    if not hmac.compare_digest(expected_sig, provided_sig):
        raise TokenDecodeError("Invalid token signature")

    payload_bytes = _b64url_decode(payload_b64)
    payload = json.loads(payload_bytes.decode("utf-8"))

    exp_raw = payload.get("exp")
    if exp_raw is None:
        raise TokenDecodeError("Token missing expiration")

    try:
        exp = int(exp_raw)
    except (TypeError, ValueError) as exc:
        raise TokenDecodeError("Invalid token expiration") from exc

    now_ts = int(datetime.now(timezone.utc).timestamp())
    if exp < now_ts:
        raise TokenDecodeError("Token has expired")

    return payload


def hash_password(password: str) -> str:
    """Create a salted PBKDF2 hash string for password storage."""

    iterations = 200_000
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    return f"pbkdf2_sha256${iterations}${salt}${digest.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against a PBKDF2 hash string."""

    try:
        algorithm, iterations_raw, salt, digest_hex = hashed_password.split("$")
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    try:
        iterations = int(iterations_raw)
    except ValueError:
        return False

    expected = bytes.fromhex(digest_hex)
    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    return hmac.compare_digest(expected, candidate)


def _create_token(subject: str, role: str, token_type: str, expires_delta: timedelta) -> str:
    """Create signed token with subject and role claims."""

    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    return _encode_jwt(payload, settings.secret_key)


def create_access_token(subject: str, role: str) -> str:
    """Create short-lived access token."""

    settings = get_settings()
    return _create_token(
        subject=subject,
        role=role,
        token_type="access",
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(subject: str, role: str) -> str:
    """Create long-lived refresh token."""

    settings = get_settings()
    return _create_token(
        subject=subject,
        role=role,
        token_type="refresh",
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict[str, Any]:
    """Decode token and return payload claims."""

    settings = get_settings()
    return _decode_jwt(token, settings.secret_key)
