"""
run_pipeline.py

Purpose
-------
Execute the complete data engineering pipeline.

Pipeline Flow
-------------
1. Find monthly ZIP archives.
2. Extract ZIP archives.
3. Read one CSV at a time.
4. Append directly to traffic_2025.csv.
5. Release memory.
"""

import gc
import zipfile

from src.data_engineering.logger import logger

from src.data_engineering.config import (
    RAW_DATA_DIR,
    TEMP_DATA_DIR,
    PROCESSED_DATA_DIR,
)

from src.data_engineering.ingestion import (
    read_csv_file,
)

from src.data_engineering.data_merger import (
    initialize_output_file,
    append_dataframe_to_csv,
)


def main() -> None:
    """
    Execute the complete data engineering pipeline.
    """

    logger.info("=" * 70)
    logger.info("Starting Smart Traffic Data Engineering Pipeline")
    logger.info("=" * 70)

    try:

        # ---------------------------------------------------------
        # Step 1 : Find all ZIP files
        # ---------------------------------------------------------
        zip_files = sorted(
            RAW_DATA_DIR.glob("*.zip")
        )

        if not zip_files:

            logger.error("No ZIP files found.")

            raise FileNotFoundError(
                f"No ZIP files found inside {RAW_DATA_DIR}"
            )

        logger.info(
            f"Found {len(zip_files)} monthly ZIP files."
        )

        # ---------------------------------------------------------
        # Step 2 : Create fresh output CSV
        # ---------------------------------------------------------
        output_path = (
            PROCESSED_DATA_DIR /
            "traffic_2025.csv"
        )

        initialize_output_file(
            output_path
        )

        # ---------------------------------------------------------
        # Step 3 : Process every ZIP
        # ---------------------------------------------------------
        for zip_file in zip_files:

            logger.info(
                f"Processing {zip_file.name}"
            )

            extract_path = (
                TEMP_DATA_DIR /
                zip_file.stem
            )

            extract_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            with zipfile.ZipFile(
                zip_file,
                "r",
            ) as archive:

                archive.extractall(
                    extract_path
                )

            logger.info(
                f"Extracted {zip_file.name}"
            )

            csv_files = sorted(
                extract_path.glob("*.csv")
            )

            logger.info(
                f"Found {len(csv_files)} CSV files."
            )

            # -------------------------------------------------
            # Step 4 : Process every CSV
            # -------------------------------------------------
            for csv_file in csv_files:

                logger.info(
                    f"Reading {csv_file.name}"
                )

                df = read_csv_file(
                    csv_file
                )

                append_dataframe_to_csv(
                    df,
                    output_path,
                )

                # Free RAM
                del df
                gc.collect()

        logger.info("=" * 70)
        logger.info(
            "Pipeline completed successfully."
        )
        logger.info("=" * 70)

    except Exception:

        logger.exception(
            "Pipeline execution failed."
        )

        raise


if __name__ == "__main__":
    main()