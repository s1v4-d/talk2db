"""Ingest files from Microsoft SharePoint."""

from typing import List
from llama_index.core import Document
from llama_index.readers.microsoft_sharepoint import SharePointReader
from .base import BaseIngestor


class SharePointIngestor(BaseIngestor):
    """Loads files from a SharePoint document library."""

    def load(self, **kwargs) -> List[Document]:
        reader = SharePointReader(
            client_id=kwargs["client_id"],
            client_secret=kwargs["client_secret"],
            tenant_id=kwargs["tenant_id"],
            site_name=kwargs["site_name"],
            drive_id=kwargs.get("drive_id"),
        )
        folder = kwargs.get("folder_path", "/")
        docs = reader.load_data(folder_path=folder)
        for doc in docs:
            doc.metadata.setdefault("source", "sharepoint")
            # Many SharePoint docs have 'file_path' metadata
            doc.metadata.setdefault(
                "path",
                doc.metadata.get("file_path", "sharepoint"),
            )
        return docs