"""Chat endpoints implementing agentic interaction."""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from ...models.schemas import ChatRequest
from ...services.agent import build_agent
from ...core.memory import get_memory
from ...utils.sse import stream_tokens
from ..dependencies import auth_dep

router = APIRouter(prefix="/chat", tags=["chat"], dependencies=[Depends(auth_dep)])


@router.post("")
def chat(req: ChatRequest):
    """
    Run a single turn of chat with the agent. Supports arbitrary data
    sources and scopes. Maintains session memory across requests.
    """
    agent = build_agent(req.scope, req.sources, req.use_hybrid, req.db_name)
    memory = get_memory(req.session_id or "default")
    result = agent.chat(req.query, memory=memory)
    citations = []
    for n in getattr(result, "source_nodes", []):
        citations.append(
            {
                "source": n.node.metadata.get("source"),
                "path": n.node.metadata.get("path"),
                "doc_id": n.node.node_id,
                "score": getattr(n, "score", None),
            }
        )
    return {"answer": str(result), "citations": citations, "artifacts": {}}


@router.get("/stream")
def chat_stream(
    query: str = Query(..., description="The user question"),
    session_id: str | None = Query(None, description="Session identifier"),
    scope: str = Query("all", description="Query scope: sql, vector, all, kg"),
    sources: str = Query("", description="Comma‑separated list of sources"),
    use_hybrid: bool = Query(True, description="Enable hybrid retrieval"),
    db_name: str | None = Query(None, description="Name of registered SQL database"),
):
    """
    Stream a chat response token by token using Server‑Sent Events. The
    parameters mirror those of the POST /chat endpoint. The response
    content type is text/event‑stream.
    """
    srcs = [s for s in sources.split(",") if s]
    agent = build_agent(scope, srcs, use_hybrid, db_name)
    memory = get_memory(session_id or "default")
    token_generator = agent.stream_chat(query, memory=memory)
    return stream_tokens(token_generator)