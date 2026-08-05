"""

Purpose
-------
Execute the complete data engineering pipeline.

Pipeline Flow
-------------
1. Find all monthly ZIP archives.
2. Extract ZIP archives into the temporary directory.
3. Read all CSV files.
4. Merge all DataFrames.
5. Save the merged dataset.
"""

import zipfile

from src.data_engineering.logger import logger
from src.data_engineering.config import (
    RAW_DATA_DIR,
    TEMP_DATA_DIR,
    PROCESSED_DATA_DIR,
)

from src.data_engineering.ingestion import (
    read_csv_folder,
)

from src.data_engineering.data_merger import (
    merge_dataframes,
    save_merged_dataset,
)


def main() -> None:
    """
    Execute the complete data engineering pipeline.
    """

    logger.info("=" * 70)
    logger.info("Starting Smart Traffic Data Engineering Pipeline")
    logger.info("=" * 70)

    try:

        # Step 1 : Find all monthly ZIP archives
        zip_files = sorted(RAW_DATA_DIR.glob("*.zip"))

        if not zip_files:

            logger.error("No ZIP files found.")

            raise FileNotFoundError(
                f"No ZIP files found inside '{RAW_DATA_DIR}'."
            )

        logger.info(
            f"Found {len(zip_files)} monthly ZIP files."
        )

        # Store every DataFrame from every month.
        yearly_dataframes = []

        # Step 2 : Extract every ZIP archive
        for zip_file in zip_files:

            extract_path = TEMP_DATA_DIR / zip_file.stem

            extract_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            logger.info(
                f"Extracting '{zip_file.name}'..."
            )

            with zipfile.ZipFile(zip_file, "r") as archive:

                archive.extractall(extract_path)

            logger.info(
                f"Successfully extracted '{zip_file.name}'."
            )

            # Step 3 : Read all CSV files from extracted folder
            monthly_dataframes = read_csv_folder(
                extract_path
            )

            yearly_dataframes.extend(
                monthly_dataframes
            )

        # Step 4 : Merge all DataFrames
        logger.info(
            "Merging all monthly DataFrames..."
        )

        merged_df = merge_dataframes(
            yearly_dataframes
        )

        # Step 5 : Save merged dataset
        output_path = (
            PROCESSED_DATA_DIR /
            "traffic_2025.csv"
        )

        save_merged_dataset(
            merged_df,
            output_path,
        )

        logger.info("=" * 70)
        logger.info("Pipeline completed successfully.")
        logger.info("=" * 70)

    except Exception:

        logger.exception(
            "Pipeline execution failed."
        )

        raise


if __name__ == "__main__":
    main()