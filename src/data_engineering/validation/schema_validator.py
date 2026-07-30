# Purpose:
# Validate the structure (schema) of a dataset.

import pandas as pd

from src.data_engineering.logger import logger
from src.data_engineering.validation.validation_result import (
    ValidationResult,
)


# Validate required columns.

def validate_columns(
    df: pd.DataFrame,
    expected_columns: list[str],
    result: ValidationResult,
) -> ValidationResult:
    """
    Validate that all required columns exist.
    """

    expected = set(expected_columns)
    actual = set(df.columns)

    missing_columns = expected - actual
    unexpected_columns = actual - expected

    if missing_columns:

        result.add_error(
            f"Missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if unexpected_columns:

        result.add_warning(
            f"Unexpected columns: "
            f"{sorted(unexpected_columns)}"
        )

    if result.passed:
        logger.info("Schema validation passed.")
    else:
        logger.error("Schema validation failed.")

    return result