"""Configuration for Talk‑To‑DB loaded from environment variables."""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    """Strongly typed settings loaded from environment variables."""

    # Authentication
    APP_API_KEY: str = os.getenv("APP_API_KEY", "dev-token")

    # LLM configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_EMBED_MODEL: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    OPENAI_EMBED_DIM: int = int(os.getenv("OPENAI_EMBED_DIM", "1536"))

    # Vector backend selection: pgvector or neo4j_vectors
    VECTOR_BACKEND: str = os.getenv("VECTOR_BACKEND", "pgvector")

    # Postgres / pgvector configuration
    POSTGRES_URI: str = os.getenv("POSTGRES_URI", "postgresql+psycopg2://postgres:postgres@db:5432/postgres")
    PGVECTOR_SCHEMA: str = os.getenv("PGVECTOR_SCHEMA", "public")
    COLLECTION_PREFIX: str = os.getenv("COLLECTION_PREFIX", "ttdb_")

    # Neo4j configuration
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "password")
    NEO4J_DB: str = os.getenv("NEO4J_DB", "neo4j")
    ENABLE_KG: bool = os.getenv("ENABLE_KG", "true").lower() == "true"

    # Retrieval defaults
    MAX_TOP_K: int = int(os.getenv("MAX_TOP_K", "10"))


settings = Settings()