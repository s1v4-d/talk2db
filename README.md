# Talk‑To‑DB Backend

This repository contains the backend and a simple Streamlit front‑end for **Talk‑To‑DB**,
an enterprise‑grade conversational agent that lets end‑users query both
structured (SQL) and unstructured (documents) data using natural language.

## Features

- **Multi‑source ingestion**: connectors for Confluence, SharePoint, OneDrive, Teams and
  arbitrary SQL databases. Each source is stored in its own vector collection.
- **Hybrid retrieval**: combine dense vector search with BM25 keyword search for
  improved relevance.
- **Dynamic query routing**: automatically choose between SQL, vector, graph or
  hybrid engines based on the user request.
- **Graph RAG support**: optional Neo4j knowledge graph for advanced
  entity/relation queries.
- **Agentic chat**: built with LlamaIndex ReAct agent and OpenAI function
  calling. Supports normal and streaming responses.
- **Data export & visualisation**: generate Excel spreadsheets from SQL queries
  and simple plots using Plotly.
- **Per‑session memory**: maintain conversation context with a memory buffer and
  lightweight cache.
- **Pluggable LLMs**: swap out OpenAI for other models by changing the config.

## Layout

```
talk2db/
├─ backend/           # FastAPI service and ingestion/query engines
│  ├─ app/
│  │  ├─ api/         # API routers and dependencies
│  │  ├─ core/        # configuration, auth, logging, llm and store abstractions
│  │  ├─ services/    # ingestion pipelines, query engines, agents
│  │  ├─ models/      # Pydantic schemas
│  │  ├─ utils/       # helper functions (e.g. SSE streaming)
│  │  └─ main.py      # entry point
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ pyproject.toml
├─ frontend/
│  ├─ app.py          # minimal Streamlit demo that calls the backend
│  └─ Dockerfile
├─ docker-compose.yml # orchestrates Postgres, Neo4j, backend and frontend
├─ Makefile           # convenience tasks
└─ .env.example       # sample environment variables
```

## Quick start

1. Copy `.env.example` to `.env` and adjust the values (OpenAI keys, DB URLs,…).
2. Build the containers:

   ```bash
   make build-docker
   ```

3. Start the stack:

   ```bash
   make start-docker
   ```

4. Index your data sources via the `/api/v1/indexing/*` endpoints and query them via
   `/api/v1/chat` or `/api/v1/search`.

See [backend/README.md](backend/README.md) for detailed API documentation.