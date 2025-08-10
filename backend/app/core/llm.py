"""Initialise LlamaIndex LLM and embedding settings."""

import os
from llama_index.core import Settings as LlamaSettings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from .config import settings

# Set OpenAI key for LlamaIndex
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# Configure LLM and embedding model via LlamaIndex
LlamaSettings.llm = OpenAI(model=settings.OPENAI_MODEL, temperature=0)
LlamaSettings.embed_model = OpenAIEmbedding(model=settings.OPENAI_EMBED_MODEL)
LlamaSettings.chunk_size = 1024