"""Ingest Confluence pages into the vector store."""

from typing import List
from llama_index.core import Document
from llama_index.readers.confluence import ConfluenceReader
from .base import BaseIngestor


class ConfluenceIngestor(BaseIngestor):
    """Loads pages and attachments from an Atlassian Confluence space."""

    def load(self, **kwargs) -> List[Document]:
        reader = ConfluenceReader(
            base_url=kwargs["base_url"],
            username=kwargs["username"],
            api_token=kwargs["api_token"],
            cloud=kwargs.get("cloud", True),
        )
        space_key = kwargs["space_key"]
        docs = reader.load_data(space_key=space_key, include_attachments=True)
        for doc in docs:
            doc.metadata.setdefault("source", "confluence")
            doc.metadata.setdefault(
                "path",
                f"{kwargs['base_url']}/spaces/{space_key}",
            )
        return docs