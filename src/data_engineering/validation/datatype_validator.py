# Purpose:
# Validate that dataset columns have the expected data types.

import pandas as pd

from src.data_engineering.logger import logger
from src.data_engineering.validation.validation_result import (
    ValidationResult,
)


# Validate column data types.

def validate_dtypes(
    df: pd.DataFrame,
    expected_dtypes: dict[str, str],
    result: ValidationResult,
) -> ValidationResult:
    """
    Validate that each column has the expected datatype.
    """

    for column, expected_dtype in expected_dtypes.items():

        actual_dtype = str(df[column].dtype)

        if actual_dtype != expected_dtype:

            result.add_error(
                f"Column '{column}' has datatype "
                f"'{actual_dtype}', expected '{expected_dtype}'."
            )

    if result.passed:
        logger.info("Datatype validation passed.")
    else:
        logger.error("Datatype validation failed.")

    return result