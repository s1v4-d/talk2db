"""Ingest channel messages from Microsoft Teams."""

from typing import List
from llama_index.core import Document
from .base import BaseIngestor


class TeamsIngestor(BaseIngestor):
    """
    Fetch messages from a specific team and channel via Microsoft Graph API.
    Requires an access token with `ChannelMessage.Read.All` permission.
    """

    def load(self, **kwargs) -> List[Document]:
        import requests

        token = kwargs["access_token"]
        team_id = kwargs["team_id"]
        channel_id = kwargs["channel_id"]
        url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/messages"
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get(url, headers=headers, timeout=60)
        res.raise_for_status()
        msgs = res.json().get("value", [])
        docs: List[Document] = []
        for m in msgs:
            content = m.get("body", {}).get("content", "")
            msg_id = m.get("id")
            path = f"teams://{team_id}/{channel_id}/{msg_id}"
            doc = Document(text=content, metadata={"source": "teams", "path": path})
            docs.append(doc)
        return docs