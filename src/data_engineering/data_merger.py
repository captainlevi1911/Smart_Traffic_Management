"""

Purpose
-------
Write DataFrames incrementally to a single CSV file.
Designed for large datasets that cannot fit entirely in memory.
"""

from pathlib import Path
import pandas as pd

from src.data_engineering.logger import logger


def create_output_file(output_path: Path) -> None:
    """
    Remove an existing output file so every pipeline run
    starts with a fresh dataset.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        output_path.unlink()
        logger.info(f"Removed existing file: {output_path.name}")


def append_dataframe_to_csv(
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Append a DataFrame to the output CSV.

    Header is written only once.
    """

    write_header = not output_path.exists()

    df.to_csv(
        output_path,
        mode="a",
        index=False,
        header=write_header,
    )

    logger.info(
        f"Appended {len(df):,} rows to '{output_path.name}'."
    )