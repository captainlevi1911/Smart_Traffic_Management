"""

Purpose:
Centralized data ingestion module.

Responsibilities:
1. Read a single CSV file.
2. Read multiple CSV files.
3. Read every CSV inside a folder.

NOTE:
This module DOES NOT merge datasets.
Merging is handled separately in data_merger.py.
"""

from pathlib import Path
import pandas as pd
from src.data_engineering.logger import logger
from typing import Iterator


# Read a single CSV file.
def read_csv_file(file_path: Path) -> pd.DataFrame:
    """
    Read a CSV file and return it as a pandas DataFrame.

    Parameters
    ----------
    file_path : Path
        Path to the CSV file.

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
    """

    try:

        # Check whether the file exists.
        if not file_path.exists():

            logger.error(f"File not found: {file_path}")

            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        # Allow only CSV files.
        if file_path.suffix.lower() != ".csv":

            logger.error(
                f"Unsupported file type: {file_path}"
            )

            raise ValueError(
                f"Expected '.csv' file, "
                f"received '{file_path.suffix}'."
            )

        # Reject empty files.
        if file_path.stat().st_size == 0:

            logger.error(
                f"CSV file is empty: {file_path}"
            )

            raise ValueError(
                f"CSV file is empty: {file_path}"
            )

        logger.info(
            f"Reading CSV file: {file_path.name}"
        )

        df = pd.read_csv(file_path)

        logger.info(
            f"Successfully loaded "
            f"{file_path.name} "
            f"({len(df):,} rows, "
            f"{len(df.columns)} columns)."
        )

        return df

    except Exception:

        logger.exception(
            f"Failed to read CSV file: {file_path}"
        )

        raise


# Read multiple CSV files.
def read_csv_files(
    file_paths: list[Path],
) -> list[pd.DataFrame]:
    """
    Read multiple CSV files.

    Parameters
    ----------
    file_paths : list[Path]
        List of CSV file paths.

    Returns
    -------
    list[pd.DataFrame]
        List of loaded DataFrames.
    """

    dataframes = []

    for file_path in file_paths:

        df = read_csv_file(file_path)

        dataframes.append(df)

    logger.info(
        f"Successfully loaded "
        f"{len(dataframes)} CSV files."
    )

    return dataframes


# Read every CSV file inside one folder.
def read_csv_folder(
    folder_path: Path,
) -> list[pd.DataFrame]:
    """
    Read all CSV files inside a folder.

    Parameters
    ----------
    folder_path : Path
        Folder containing CSV files.

    Returns
    -------
    list[pd.DataFrame]
        List of DataFrames.

    Raises
    ------
    FileNotFoundError
        If the folder does not exist.

    ValueError
        If no CSV files are found.
    """

    # Validate folder.
    if not folder_path.exists():

        logger.error(
            f"Folder not found: {folder_path}"
        )

        raise FileNotFoundError(
            f"Folder not found: {folder_path}"
        )

    csv_files = sorted(
        folder_path.glob("*.csv")
    )

    if not csv_files:

        logger.error(
            f"No CSV files found in "
            f"{folder_path}"
        )

        raise ValueError(
            f"No CSV files found in "
            f"{folder_path}"
        )

    logger.info(
        f"Found {len(csv_files)} CSV files "
        f"in '{folder_path.name}'."
    )

    return read_csv_files(csv_files)


def read_csv_in_chunks(
    file_path: Path,
    chunk_size: int = 25_000,
) -> Iterator[pd.DataFrame]:
    """
    Read a CSV file in chunks.

    Parameters
    ----------
    file_path : Path
        Path to the CSV file.

    chunk_size : int, default=25000
        Number of rows to load at one time.

    Yields
    ------
    pd.DataFrame
        One chunk of the CSV at a time.
    """

    try:

        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() != ".csv":
            logger.error(f"Unsupported file type: {file_path}")
            raise ValueError(
                f"Expected CSV file but got {file_path.suffix}"
            )

        if file_path.stat().st_size == 0:
            logger.error(f"CSV file is empty: {file_path}")
            raise ValueError(f"CSV file is empty: {file_path}")

        logger.info(
            f"Reading '{file_path.name}' in chunks of {chunk_size:,} rows."
        )

        for chunk in pd.read_csv(
            file_path,
            chunksize=chunk_size,
            low_memory=False,
        ):

            yield chunk

    except Exception:

        logger.exception(
            f"Failed to read CSV in chunks: {file_path}"
        )

        raise