"""Construction of an agentic chat engine using LlamaIndex tools."""

from typing import Any, Dict, List
import pandas as pd
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from .query_engines import router_engine
from .export import dataframe_to_excel
from .ingestion.database import sql_registry


def _search_tool(
    query: str,
    scope: str,
    sources: List[str],
    use_hybrid: bool,
    db_name: str | None = None,
) -> Dict[str, Any]:
    """
    Search over the selected sources using the appropriate query engine and
    return the answer along with citation data.
    """
    qe = router_engine(scope=scope, sources=sources, use_hybrid=use_hybrid, db_name=db_name)
    resp = qe.query(query)
    citations = []
    for n in getattr(resp, "source_nodes", []):
        citations.append(
            {
                "text": n.node.get_content()[:200],
                "score": getattr(n, "score", None),
                "source": n.node.metadata.get("source"),
                "path": n.node.metadata.get("path"),
                "doc_id": n.node.node_id,
            }
        )
    return {"answer": str(resp), "citations": citations}


def _ask_sql(query: str, db_name: str) -> Dict[str, Any]:
    """Execute a natural language SQL query and return the answer and SQL."""
    qe = router_engine(scope="sql", sources=[], use_hybrid=False, db_name=db_name)
    resp = qe.query(query)
    return {
        "answer": str(resp),
        "sql": getattr(resp, "metadata", {}).get("sql_query"),
    }


def _plot(columns: List[str], rows: List[List[Any]], kind: str = "line") -> str:
    """
    Create a simple plot using Plotly given a list of columns and rows.
    Returns the path to an HTML file containing the plot.
    """
    import plotly.express as px
    df = pd.DataFrame(rows, columns=columns)
    # Select a chart based on the requested kind
    if kind == "bar":
        fig = px.bar(df, x=columns[0], y=columns[1:])
    elif kind == "scatter":
        fig = px.scatter(df, x=columns[0], y=columns[1:])
    else:
        fig = px.line(df, x=columns[0], y=columns[1:])
    out_path = "/tmp/plot.html"
    fig.write_html(out_path)
    return out_path


def _export_sql_excel(columns: List[str], rows: List[List[Any]]) -> str:
    """Create an Excel file from rows/columns and return its path."""
    df = pd.DataFrame(rows, columns=columns)
    return dataframe_to_excel(df)


def build_agent(scope: str, sources: List[str], use_hybrid: bool, db_name: str | None):
    """
    Build a ReAct agent with tools for document search, SQL queries, Excel
    export and plotting. Tools are registered as OpenAI function tools.
    """
    tools = []
    # Search tool
    tools.append(
        FunctionTool.from_defaults(
            fn=lambda q: _search_tool(q, scope, sources, use_hybrid, db_name),
            name="search_documents",
            description="Search selected data sources and return answer with citations.",
        )
    )
    # SQL tools if any DB registered
    if sql_registry.engines:
        tools.append(
            FunctionTool.from_defaults(
                fn=lambda q: _ask_sql(q, db_name or next(iter(sql_registry.engines))),
                name="ask_sql",
                description="Ask a question to the SQL database and get back the answer and SQL.",
            )
        )
        tools.append(
            FunctionTool.from_defaults(
                fn=_export_sql_excel,
                name="export_sql_excel",
                description="Export tabular rows and columns to an Excel file.",
            )
        )
    # Plot tool
    tools.append(
        FunctionTool.from_defaults(
            fn=_plot,
            name="plot",
            description="Create a simple line/bar/scatter plot from tabular data.",
        )
    )
    return ReActAgent.from_tools(tools)