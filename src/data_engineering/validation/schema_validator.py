# Purpose:
# Validate the structure (schema) of a dataset before it enters
# the data cleaning and machine learning pipeline.

import pandas as pd

from src.data_engineering.logger import logger


# Validate that all required columns are present in the dataset.

def validate_columns(
    df: pd.DataFrame,
    expected_columns: list[str],
) -> None:
    """
    Validate the dataset schema by checking required columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.

    expected_columns : list[str]
        List of columns that must exist in the dataset.

    Raises
    ------
    ValueError
        If one or more required columns are missing.
    """

    expected = set(expected_columns)
    actual = set(df.columns)

    missing_columns = expected - actual
    unexpected_columns = actual - expected

    # Missing required columns should stop the pipeline.
    if missing_columns:
        logger.error(
            f"Missing columns: {sorted(missing_columns)}"
        )

        raise ValueError(
            f"Dataset is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    # Extra columns are logged as a warning because they
    # may come from a newer dataset version.
    if unexpected_columns:
        logger.warning(
            f"Unexpected columns found: "
            f"{sorted(unexpected_columns)}"
        )

    logger.info("Schema validation completed successfully.")