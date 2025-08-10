"""FastAPI entry point for Talk‑To‑DB."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import llm  # noqa: F401 ensure LLM config is loaded
from .api.routers import health, indexing, search, chat, sql, admin

app = FastAPI(title="Talk‑To‑DB Backend", version="0.1.0")

# Allow all origins for demo purposes; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(indexing.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(sql.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")