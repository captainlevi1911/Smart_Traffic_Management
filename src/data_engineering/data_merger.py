# Purpose:
# Merge multiple CSV files into a single DataFrame.

from pathlib import Path
import pandas as pd
from src.data_engineering.logger import logger

def merge_csv_files(
    folder_path: Path,
) -> pd.DataFrame:

    if not folder_path.exists():

        logger.error(f"Folder not found: {folder_path}")

        raise FileNotFoundError(
            f"Folder does not exist: {folder_path}"
        )

    csv_files = sorted(
        folder_path.glob("*.csv")
    )

    if not csv_files:

        logger.error(
            f"No CSV files found in: {folder_path}"
        )

        raise ValueError(
            f"No CSV files found in: {folder_path}"
        )