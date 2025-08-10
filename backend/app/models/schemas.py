"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Any

# Query scopes supported by the query engine
Scope = Literal["sql", "vector", "all", "kg"]


class IndexRequest(BaseModel):
    """Request payload for indexing documents."""

    source: Literal["confluence", "sharepoint", "onedrive", "teams"]
    config: dict


class SQLRegisterRequest(BaseModel):
    """Request payload for registering a SQL database."""

    name: str = "default"
    dsn: str
    include_tables: Optional[List[str]] = None
    schema: Optional[str] = None


class SearchRequest(BaseModel):
    """
    Request model for search and SQL endpoints. It is used for search,
    chat, and direct SQL queries. Additional fields may be ignored by
    certain endpoints.
    """
    query: str
    sources: List[str] = Field(default_factory=list)
    scope: Scope = "vector"
    use_hybrid: bool = True
    db_name: Optional[str] = None
    top_k: int = 5
    session_id: Optional[str] = None


class ChatRequest(SearchRequest):
    """Request model for chat interactions."""
    stream: bool = False


class ChatResponse(BaseModel):
    """Response model for chat interactions."""
    answer: str
    citations: list[Any] = []
    artifacts: dict[str, Any] = {}