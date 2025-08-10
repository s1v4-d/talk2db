"""Simple API key authentication for FastAPI routes."""

from fastapi import Header, HTTPException, status
from .config import settings


async def require_api_key(
    authorization: str | None = Header(None), x_api_key: str | None = Header(None)
) -> bool:
    """
    Validate an incoming API token. Accepts either a bearer token in the
    `Authorization` header or `X-API-Key` header. Returns True on success
    or raises HTTP 401 on failure.
    """
    token: str | None = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    elif x_api_key:
        token = x_api_key.strip()
    if token != settings.APP_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
    return True