"""Utility functions for working with pgvector via LlamaIndex."""

from sqlalchemy import create_engine
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
from .config import settings


_engine = create_engine(settings.POSTGRES_URI, pool_pre_ping=True)


def collection_name(source: str) -> str:
    """Compute the table name for a given source collection."""
    return f"{settings.COLLECTION_PREFIX}{source}"


def get_pgvector_index(index_name: str) -> VectorStoreIndex:
    """
    Return (and create if necessary) a VectorStoreIndex backed by pgvector.
    The table is created in the configured schema and uses the embedding
    dimension from settings.
    """
    vs = PGVectorStore.from_params(
        engine=_engine,
        schema_name=settings.PGVECTOR_SCHEMA,
        table_name=index_name,
        embed_dim=settings.OPENAI_EMBED_DIM,
    )
    sc = StorageContext.from_defaults(vector_store=vs)
    return VectorStoreIndex.from_vector_store(vector_store=vs, storage_context=sc)


def index_for_source(source: str) -> VectorStoreIndex:
    """Convenience function to get an index for a specific source."""
    return get_pgvector_index(collection_name(source))