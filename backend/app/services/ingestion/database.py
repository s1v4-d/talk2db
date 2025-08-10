"""Registry for SQL database connections and structured query engines."""

from sqlalchemy import create_engine
from llama_index.core import SQLDatabase


class SQLRegistry:
    """
    Maintain a mapping from names to LlamaIndex SQLDatabase objects. This
    provides a simple way to register multiple databases and reference them
    by name in query requests.
    """

    def __init__(self) -> None:
        self.engines: dict[str, SQLDatabase] = {}

    def register(
        self,
        name: str,
        dsn: str,
        include: list[str] | None = None,
        schema: str | None = None,
    ) -> str:
        engine = create_engine(dsn)
        sqldb = SQLDatabase(engine, include_tables=include, schema=schema)
        self.engines[name] = sqldb
        return name

    def get(self, name: str) -> SQLDatabase:
        return self.engines[name]


sql_registry = SQLRegistry()