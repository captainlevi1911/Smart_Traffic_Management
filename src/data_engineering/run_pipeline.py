"""
run_pipeline.py

Purpose
-------
Execute the complete Smart Traffic data engineering pipeline.

Pipeline
--------
1. Find monthly ZIP archives.
2. Extract ZIP archives.
3. Read one CSV at a time.
4. Append each DataFrame to traffic_2025.csv.
5. Release memory.
6. Log detailed information for debugging.
"""

import gc
import os
import zipfile

import psutil

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


def log_memory():
    """
    Log current RAM usage of the Python process.
    """

    process = psutil.Process(os.getpid())

    ram = process.memory_info().rss / (1024 ** 2)

    logger.info(f"Current Process RAM Usage : {ram:.2f} MB")


def main():

    logger.info("=" * 70)
    logger.info("Starting Smart Traffic Data Engineering Pipeline")
    logger.info("=" * 70)

    try:

        # ==========================================================
        # Step 1 : Find ZIP files
        # ==========================================================
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

        # ==========================================================
        # Step 2 : Create Output File
        # ==========================================================
        output_path = (
            PROCESSED_DATA_DIR /
            "traffic_2025.csv"
        )

        initialize_output_file(output_path)

        # ==========================================================
        # Step 3 : Process every ZIP archive
        # ==========================================================
        for month_index, zip_file in enumerate(
            zip_files,
            start=1,
        ):

            logger.info("")
            logger.info("=" * 70)
            logger.info(
                f"Processing Month {month_index}/{len(zip_files)}"
            )
            logger.info(
                f"Archive : {zip_file.name}"
            )
            logger.info("=" * 70)

            extract_path = (
                TEMP_DATA_DIR /
                zip_file.stem
            )

            extract_path.mkdir(
                parents=True,
                exist_ok=True,
            )

            logger.info(
                f"Extracting {zip_file.name}"
            )

            with zipfile.ZipFile(
                zip_file,
                "r",
            ) as archive:

                archive.extractall(
                    extract_path
                )

            logger.info(
                "Extraction completed."
            )

            csv_files = sorted(
                extract_path.glob("*.csv")
            )

            logger.info(
                f"Found {len(csv_files)} CSV files."
            )

            # ======================================================
            # Step 4 : Process every CSV
            # ======================================================
            for csv_index, csv_file in enumerate(
                csv_files,
                start=1,
            ):

                logger.info("")
                logger.info("-" * 60)
                logger.info(
                    f"CSV {csv_index}/{len(csv_files)}"
                )
                logger.info(
                    f"Current File : {csv_file.name}"
                )

                log_memory()

                # ----------------------------------------------
                # Read CSV
                # ----------------------------------------------
                df = read_csv_file(csv_file)

                logger.info(
                    f"Shape : {df.shape}"
                )

                dataframe_memory = (
                    df.memory_usage(deep=True)
                    .sum()
                    / (1024 ** 2)
                )

                logger.info(
                    f"DataFrame Memory : "
                    f"{dataframe_memory:.2f} MB"
                )

                log_memory()

                # ----------------------------------------------
                # Append to output CSV
                # ----------------------------------------------
                append_dataframe_to_csv(
                    df,
                    output_path,
                )

                logger.info(
                    "Successfully appended."
                )

                # ----------------------------------------------
                # Free Memory
                # ----------------------------------------------
                del df

                gc.collect()

                logger.info(
                    "Released DataFrame memory."
                )

                log_memory()

        logger.info("")
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