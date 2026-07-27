# ingestion.py

# Purpose:
# Centralized data ingestion module for reading CSV files.
# All project modules should use this file instead of calling
# pandas.read_csv() directly.


import pandas as pd
from pathlib import Path

from src.data_engineering.logger import logger




def read_csv_file(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file and return it as a pandas DataFrame.

    Parameters
    ----------
    file_path : Path
        Absolute or relative path of the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded dataframe.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.

    ValueError
        If the file is not a CSV or is empty.

    Exception
        Any unexpected exception raised while reading the file.
    """
    
    try:

        # Ensure the file exists before attempting to read it.
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        # Accept only CSV files.
        if file_path.suffix.lower() != ".csv":
            logger.error(f"Unsupported file type: {file_path}")

            raise ValueError(
                f"Expected a CSV file, received '{file_path.suffix}' instead."
            )

        # Reject empty files early.
        if file_path.stat().st_size == 0:
            logger.error(f"CSV file is empty: {file_path}")

            raise ValueError(
                f"CSV file is empty: {file_path}"
            )

        logger.info(f"Reading CSV file: {file_path}")

        df = pd.read_csv(file_path)

        logger.info(
            f"Successfully loaded '{file_path.name}' "
            f"with {len(df):,} rows and {len(df.columns)} columns."
        )

        return df

    except Exception:
        logger.exception(f"Failed to read CSV file: {file_path}")
        raise

# Read multiple CSV files.

def read_multiple_csv_files(
    file_paths: list[Path],
) -> list[pd.DataFrame]:

    # Store each successfully loaded DataFrame.
    dataframes = []

    for file_path in file_paths:

        df = read_csv_file(file_path)

        dataframes.append(df)

    return dataframes

# Read every CSV file inside a folder and return one merged DataFrame.


def read_folder(folder_path: Path) -> pd.DataFrame:

    # Ensure the folder exists before searching for CSV files.
    if not folder_path.exists():
        logger.error(f"Folder not found: {folder_path}")
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    csv_files = sorted(folder_path.glob("*.csv"))

    if not csv_files:
        logger.error(f"No CSV files found in: {folder_path}")
        raise ValueError(f"No CSV files found in: {folder_path}")

    logger.info(f"Found {len(csv_files)} CSV files in '{folder_path.name}'.")

    dataframes = read_multiple_csv_files(csv_files)

    merged_df = pd.concat(
        dataframes,
        ignore_index=True
    )

    logger.info(
        f"Merged {len(dataframes)} files into one DataFrame "
        f"with {len(merged_df):,} rows."
    )

    return merged_df




    