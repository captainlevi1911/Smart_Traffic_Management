"""
data_merger.py

Purpose
-------
Incrementally write DataFrames to a single CSV file.

Instead of storing hundreds of DataFrames in memory,
we append each DataFrame directly to the output CSV.
"""

from pathlib import Path
import pandas as pd

from src.data_engineering.logger import logger


def initialize_output_file(output_path: Path) -> None:
    """
    Create a fresh output CSV.

    If the file already exists from a previous run,
    delete it first.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if output_path.exists():
        output_path.unlink()

        logger.info(
            f"Removed existing file: {output_path.name}"
        )


def append_dataframe_to_csv(
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Append a DataFrame to the output CSV.

    The header is written only once.
    """

    write_header = not output_path.exists()

    df.to_csv(
        output_path,
        mode="a",
        index=False,
        header=write_header,
    )

    logger.info(
        f"Appended {len(df):,} rows to "
        f"{output_path.name}"
    )