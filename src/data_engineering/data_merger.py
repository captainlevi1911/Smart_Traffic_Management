"""

Purpose
-------
Merge multiple pandas DataFrames into a single DataFrame
and save the merged dataset.

This module does NOT read CSV files.
Reading is handled by ingestion.py.
"""

from pathlib import Path

import pandas as pd

from src.data_engineering.logger import logger


# Merge multiple DataFrames into one DataFrame.
def merge_dataframes(
    dataframes: list[pd.DataFrame],
) -> pd.DataFrame:
    """
    Merge multiple DataFrames into one.

    Parameters
    ----------
    dataframes : list[pd.DataFrame]
        List of DataFrames to merge.

    Returns
    -------
    pd.DataFrame
        Combined DataFrame.
    """

    if not dataframes:

        logger.error("No DataFrames were provided for merging.")

        raise ValueError(
            "Cannot merge an empty list of DataFrames."
        )

    logger.info(
        f"Merging {len(dataframes)} DataFrames."
    )

    merged_df = pd.concat(
        dataframes,
        ignore_index=True,
    )

    logger.info(
        f"Merged DataFrame contains "
        f"{len(merged_df):,} rows."
    )

    return merged_df


# Save merged DataFrame.
def save_merged_dataset(
    dataframe: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Save the merged DataFrame as a CSV file.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame to save.

    output_path : Path
        Destination CSV path.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        output_path,
        index=False,
    )

    logger.info(
        f"Merged dataset saved to: {output_path}"
    )