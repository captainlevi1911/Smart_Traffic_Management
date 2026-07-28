import pandas as pd

from src.data_engineering.logger import logger


# Validate that all expected columns are present.
def validate_columns(
    df: pd.DataFrame,
    expected_columns: list[str],
) -> None: