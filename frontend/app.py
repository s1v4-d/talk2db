import streamlit as st
import requests
import os

# Basic Streamlit UI for Talk‑To‑DB
API = os.getenv("API_URL", "http://backend:8000/api/v1")
KEY = os.getenv("APP_API_KEY", "dev-token")
HEADERS = {"Authorization": f"Bearer {KEY}"}

st.title("Talk‑To‑DB Chat Interface")

# Scope and sources selection
scope = st.selectbox(
    "Select query scope",
    ["vector", "sql", "all", "kg"],
    index=2,
    format_func=lambda x: x.upper(),
)

available_sources = ["confluence", "sharepoint", "onedrive", "teams"]
sources = st.multiselect(
    "Choose data sources to search",
    available_sources,
    default=available_sources,
)

query = st.text_area("Ask your question:")

if st.button("Send"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        payload = {
            "query": query,
            "scope": scope,
            "sources": sources,
            "use_hybrid": True,
            "top_k": 5,
        }
        with st.spinner("Querying backend..."):
            try:
                resp = requests.post(f"{API}/search", json=payload, headers=HEADERS, timeout=180)
                resp.raise_for_status()
                data = resp.json()
                st.subheader("Answer")
                st.write(data.get("answer", "No answer returned"))
                if data.get("citations"):
                    st.subheader("Sources")
                    for cite in data["citations"]:
                        path = cite.get("path", "")
                        score = cite.get("score", 0.0)
                        st.write(f"• {path} (score={score:.2f})")
            except Exception as e:
                st.error(f"Error: {e}")