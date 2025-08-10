"""Helpers for inserting documents into the vector store."""

from typing import List
from llama_index.core import Document
from ..core.vectorstores import index_for_source


def upsert_documents(source: str, docs: List[Document]) -> dict:
    """
    Insert a list of documents into the vector collection for a specific
    source. Uses the configured pgvector table. Returns information about
    the operation.
    """
    index = index_for_source(source)
    index.insert_documents(docs)
    return {"source": source, "count": len(docs)}