"""Endpoints for direct SQL queries and exporting results."""

from fastapi import APIRouter, Depends, HTTPException
from ...models.schemas import SearchRequest
from ...services.query_engines import router_engine
from ...services.export import dataframe_to_excel
import pandas as pd
from ..dependencies import auth_dep

router = APIRouter(prefix="/sql", tags=["sql"], dependencies=[Depends(auth_dep)])


@router.post("/ask")
def sql_ask(req: SearchRequest):
    """
    Execute a natural language SQL query against the registered database.
    Returns the generated answer and the executed SQL query. If no database
    has been registered, raises an error.
    """
    if not req.db_name:
        raise HTTPException(status_code=400, detail="db_name is required for SQL queries")
    qe = router_engine(scope="sql", sources=[], use_hybrid=False, db_name=req.db_name)
    resp = qe.query(req.query)
    return {
        "answer": str(resp),
        "sql": getattr(resp, "metadata", {}).get("sql_query"),
    }


@router.post("/export")
def sql_export(req: SearchRequest):
    """
    Execute a SQL query and return an Excel file containing the result. The
    response includes the path of the created file. Requires db_name.
    """
    if not req.db_name:
        raise HTTPException(status_code=400, detail="db_name is required for SQL export")
    qe = router_engine(scope="sql", sources=[], use_hybrid=False, db_name=req.db_name)
    resp = qe.query(req.query)
    table = getattr(resp, "metadata", {}).get("result_table")
    if not table:
        raise HTTPException(status_code=400, detail="No tabular result returned from query")
    columns = table.get("columns", [])
    rows = table.get("rows", [])
    df = pd.DataFrame(rows, columns=columns)
    filepath = dataframe_to_excel(df)
    return {"file_path": filepath}