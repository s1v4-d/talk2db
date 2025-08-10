"""Helpers for exporting data frames to files."""

import os
import uuid
import pandas as pd


def dataframe_to_excel(df: pd.DataFrame) -> str:
    """
    Write a pandas DataFrame to an Excel file in a temporary directory and
    return its absolute path. Uses a random UUID for the filename.
    """
    out_dir = "/tmp/exports"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{uuid.uuid4().hex}.xlsx")
    df.to_excel(path, index=False)
    return path