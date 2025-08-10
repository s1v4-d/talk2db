"""FastAPI dependencies for authentication."""

from fastapi import Depends
from ..core.auth import require_api_key


def auth_dep(_: bool = Depends(require_api_key)):
    """
    Dummy dependency used to enforce API key authentication on protected
    endpoints. Returns True if the key is valid; otherwise raises an HTTP 401.
    """
    return True