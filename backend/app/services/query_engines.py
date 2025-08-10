"""Factory functions for LlamaIndex query engines."""

from typing import List, Literal, Optional
from llama_index.core.query_engine import RouterQueryEngine, CitationQueryEngine, SQLJoinQueryEngine
from llama_index.core.indices.struct_store.sql_query import NLSQLTableQueryEngine
from llama_index.core.indices.property_graph import TextToCypherRetriever
from llama_index.core.response_synthesizers import ResponseMode
from .retrieval import build_hybrid_retriever
from .ingestion.database import sql_registry
from ..core.vectorstores import index_for_source
from ..core.graph import get_neo4j_graph_store
from ..core.config import settings


def vector_query_engine(sources: List[str], use_hybrid: bool):
    """
    Build a CitationQueryEngine that retrieves from the configured vector store
    using optionally hybrid retrieval (dense + sparse). Returns an engine
    configured for compact responses with citations.
    """
    retriever = build_hybrid_retriever(sources, use_hybrid)
    return CitationQueryEngine.from_args(retriever=retriever, response_mode=ResponseMode.COMPACT)


def sql_query_engine(db_name: str) -> NLSQLTableQueryEngine:
    """Instantiate an NL SQL query engine for a registered database."""
    sqldb = sql_registry.get(db_name)
    return NLSQLTableQueryEngine(sqldb)


def kg_query_engine():
    """Return a KG query engine using Neo4j if enabled; otherwise None."""
    if not settings.ENABLE_KG:
        return None
    graph = get_neo4j_graph_store()
    retriever = TextToCypherRetriever(graph_store=graph)
    return CitationQueryEngine.from_args(retriever=retriever, response_mode=ResponseMode.COMPACT)


def router_engine(
    scope: Literal["sql", "vector", "all", "kg"],
    sources: List[str],
    use_hybrid: bool,
    db_name: Optional[str] = None,
):
    """
    Select and return an appropriate query engine based on the given scope.
    - "sql": use the NL SQL query engine for the given database
    - "vector": use the vector query engine for selected sources
    - "kg": use the knowledge graph engine if enabled, otherwise fall back to vector
    - "all": combine SQL and vector by joining results (SQLJoinQueryEngine). If no
      database is registered, returns the vector engine.
    """
    if scope == "sql":
        if not db_name:
            raise ValueError("db_name must be provided when scope='sql'")
        return sql_query_engine(db_name)
    if scope == "vector":
        return vector_query_engine(sources, use_hybrid)
    if scope == "kg":
        eng = kg_query_engine()
        return eng or vector_query_engine(sources, use_hybrid)

    # "all" – combine SQL and vector results
    if sql_registry.engines:
        # Use the first registered DB if none specified
        db = db_name or next(iter(sql_registry.engines))
        sql_eng = sql_query_engine(db)
        vec_eng = vector_query_engine(sources, use_hybrid)
        return SQLJoinQueryEngine(sql_query_engine=sql_eng, other_query_engine=vec_eng)
    # No DB registered; fallback to vector
    return vector_query_engine(sources, use_hybrid)