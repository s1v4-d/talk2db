"""Search endpoint returning answers with citations."""

from fastapi import APIRouter, Depends
from ...models.schemas import SearchRequest
from ...services.query_engines import router_engine
from ..dependencies import auth_dep

router = APIRouter(prefix="/search", tags=["search"], dependencies=[Depends(auth_dep)])


@router.post("")
def search(req: SearchRequest):
    """
    Perform a one‑shot query over the selected data sources. The request
    specifies the natural language `query`, a list of `sources`, and a
    retrieval `scope` (sql, vector, all, kg). It optionally enables
    hybrid retrieval (`use_hybrid`) and limits results to `top_k`.
    """
    qe = router_engine(
        scope=req.scope,
        sources=req.sources,
        use_hybrid=req.use_hybrid,
        db_name=req.db_name,
    )
    resp = qe.query(req.query)
    citations = []
    # Extract citation information from LlamaIndex response
    for n in getattr(resp, "source_nodes", []):
        citations.append(
            {
                "score": getattr(n, "score", None),
                "source": n.node.metadata.get("source"),
                "path": n.node.metadata.get("path"),
                "doc_id": n.node.node_id,
            }
        )
    return {"answer": str(resp), "citations": citations}