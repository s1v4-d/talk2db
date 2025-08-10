"""Support for Neo4j graph store and knowledge graph index."""

from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.core import StorageContext, KnowledgeGraphIndex
from .config import settings


def get_neo4j_graph_store() -> Neo4jGraphStore:
    """Create a Neo4jGraphStore instance using configured credentials."""
    return Neo4jGraphStore(
        username=settings.NEO4J_USER,
        password=settings.NEO4J_PASSWORD,
        url=settings.NEO4J_URI,
        database=settings.NEO4J_DB,
    )


def build_kg_index_from_docs(documents):
    """
    Build and persist a knowledge graph index from a list of documents. The
    resulting triples are stored in Neo4j. Returns the index instance.
    """
    graph_store = get_neo4j_graph_store()
    storage = StorageContext.from_defaults(graph_store=graph_store)
    return KnowledgeGraphIndex.from_documents(
        documents,
        storage_context=storage,
        max_triplets_per_chunk=2,
    )