"""Ingest files from Microsoft OneDrive."""

from typing import List
from llama_index.core import Document
from llama_index.readers.microsoft_onedrive import OneDriveReader
from .base import BaseIngestor


class OneDriveIngestor(BaseIngestor):
    """Loads files from a user's or group's OneDrive."""

    def load(self, **kwargs) -> List[Document]:
        reader = OneDriveReader(
            client_id=kwargs["client_id"],
            client_secret=kwargs["client_secret"],
            tenant_id=kwargs["tenant_id"],
        )
        principal = kwargs["user_principal_name"]
        paths = kwargs.get("paths")  # optional list of folder paths
        docs = reader.load_data(userprincipalname=principal, paths=paths)
        for doc in docs:
            doc.metadata.setdefault("source", "onedrive")
            doc.metadata.setdefault("path", doc.metadata.get("file_path", "onedrive"))
        return docs