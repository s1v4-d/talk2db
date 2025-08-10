"""Conversation memory utilities."""

from typing import Dict
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer


_chat_store = SimpleChatStore()
_sessions: Dict[str, ChatMemoryBuffer] = {}


def get_memory(session_id: str) -> ChatMemoryBuffer:
    """
    Return a ChatMemoryBuffer for the given session. Creates one if it does
    not already exist. Keeps a small token limit to avoid exceeding LLM
    context windows.
    """
    if session_id not in _sessions:
        _sessions[session_id] = ChatMemoryBuffer.from_defaults(
            chat_store=_chat_store,
            token_limit=4000,
        )
    return _sessions[session_id]