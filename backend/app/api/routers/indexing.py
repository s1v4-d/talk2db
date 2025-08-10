"""API endpoints for ingesting data sources into the vector store."""

from fastapi import APIRouter, Depends, HTTPException

from ...models.schemas import IndexRequest, SQLRegisterRequest
from ...services.ingestion.confluence import ConfluenceIngestor
from ...services.ingestion.sharepoint import SharePointIngestor
from ...services.ingestion.onedrive import OneDriveIngestor
from ...services.ingestion.teams import TeamsIngestor
from ...services.ingestion.database import sql_registry
from ...services.indexing import upsert_documents
from ...core.config import settings
from ..dependencies import auth_dep

router = APIRouter(prefix="/indexing", tags=["indexing"], dependencies=[Depends(auth_dep)])

# Registry mapping for source types
_INGESTORS = {
    "confluence": ConfluenceIngestor(),
    "sharepoint": SharePointIngestor(),
    "onedrive": OneDriveIngestor(),
    "teams": TeamsIngestor(),
}


@router.post("/{source}")
def index_source(payload: IndexRequest):
    """
    Index data from the specified source. The payload must include a
    `config` dictionary with connection details and scope parameters. For
    example, for Confluence:
    `{ "source": "confluence", "config": {"base_url": "...", "username": "...", "api_token": "...", "space_key": "..."} }`.
    """
    source = payload.source
    if source not in _INGESTORS:
        raise HTTPException(status_code=400, detail=f"Unsupported source: {source}")
    ingestor = _INGESTORS[source]
    try:
        docs = ingestor.load(**payload.config)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    result = upsert_documents(source, docs)
    return {"indexed": result}


@router.post("/sql/register")
def sql_register(req: SQLRegisterRequest):
    """
    Register a SQL data source. Provide a DSN (SQLAlchemy URI) and optional
    list of tables or schema. The returned name can be used in query
    requests to specify which database to query.
    """
    name = sql_registry.register(req.name, req.dsn, req.include_tables, req.schema)
    return {"registered": name}