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

    # Store each CSV as a DataFrame.
    dataframes = []

    for csv_file in csv_files:

        logger.info(
            f"Reading file: {csv_file.name}"
        )

        try:

            df = pd.read_csv(csv_file)

        except Exception as e:

            logger.error(
                f"Failed to read "
                f"{csv_file.name}: {e}"
            )

            raise

        dataframes.append(df)

    merged_df = pd.concat(
        dataframes,
        ignore_index=True,
    )

    logger.info(
        f"Successfully merged "
        f"{len(csv_files)} CSV files."
    )

    return merged_df