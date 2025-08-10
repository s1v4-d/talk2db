"""Assembly of retrieval pipelines for hybrid search."""

from typing import List
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import BM25Retriever, QueryFusionRetriever
from ..core.vectorstores import index_for_source
from ..core.config import settings


def get_vector_retrievers(sources: List[str]) -> List:
    """Return a list of default vector retrievers for each source."""
    retrievers = []
    for src in sources:
        idx: VectorStoreIndex = index_for_source(src)
        retrievers.append(idx.as_retriever(similarity_top_k=settings.MAX_TOP_K))
    return retrievers


def build_hybrid_retriever(sources: List[str], use_hybrid: bool):
    """
    Create a fusion retriever which optionally fuses dense and sparse search.
    If `use_hybrid` is True, a BM25 retriever is added for each index and
    results are fused using reciprocal rank fusion. Otherwise only the
    vector retrievers are used.
    """
    retrievers = get_vector_retrievers(sources)
    if use_hybrid:
        # Add a BM25 retriever per index to capture lexical matches
        for src in sources:
            idx = index_for_source(src)
            retrievers.append(BM25Retriever.from_defaults(index=idx))
        return QueryFusionRetriever(retrievers=retrievers, num_queries=1, mode="reciprocal_rerank")
    return QueryFusionRetriever(retrievers=retrievers, num_queries=1, mode="simple")