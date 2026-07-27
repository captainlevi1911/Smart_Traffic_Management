# Importing Libraries

import pandas as pd
from pathlib import Path

from src.data_engineering.logger import logger

# Read a CSV file and return it as a pandas DataFrame.
def read_csv_file(file_path: Path) -> pd.DataFrame:
    try:
        # Ensure the input file exists before attempting to read it.
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        # Log the file being processed before reading it.
        logger.info(f"Reading CSV file: {file_path}")

        df = pd.read_csv(file_path)

        logger.info(
            f"Successfully loaded {file_path.name} "
            f"with {len(df):,} rows and {len(df.columns)} columns."
        )

        return df

    except Exception:
        logger.exception(f"Failed to read CSV file: {file_path}")
        raise