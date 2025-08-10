"""Base class for ingestion services."""

from typing import List
from llama_index.core import Document


class BaseIngestor:
    """Abstract interface for ingestion classes."""

    def load(self, **kwargs) -> List[Document]:  # pragma: no cover
        raise NotImplementedError