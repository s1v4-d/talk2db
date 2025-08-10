"""Admin and inspection endpoints."""

from fastapi import APIRouter, Depends
from ..dependencies import auth_dep

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(auth_dep)])


@router.get("/sources")
def sources():
    """Return a static list of configured source collections."""
    # In a real system this would introspect the vector store for collections
    return {"collections": ["confluence", "sharepoint", "onedrive", "teams"]}