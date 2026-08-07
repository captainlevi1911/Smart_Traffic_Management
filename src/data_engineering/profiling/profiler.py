"""
profiler.py

Purpose
-------
Profiles very large CSV datasets without loading the
entire dataset into memory.

This profiler is designed for datasets that are larger
than available RAM.

Current Version
---------------
Version 1 computes:

✓ Total rows
✓ Total columns
✓ Column names
✓ Data types
✓ Missing values
✓ File size
✓ Processing memory
"""

from pathlib import Path
import gc
import time

import pandas as pd

from src.data_engineering.logger import logger
from src.data_engineering.profiling.profile_report import (
    ProfileReport,
)


class DataProfiler:
    """
    Profiles large CSV datasets using chunk processing.
    """

    def __init__(
        self,
        dataset_path: Path,
        chunk_size: int = 100_000,
    ) -> None:

        self.dataset_path = dataset_path

        self.chunk_size = chunk_size

        self.report = ProfileReport()

    # =====================================================
    # Public Method
    # =====================================================

    def run(self) -> ProfileReport:
        """
        Execute dataset profiling.

        Returns
        -------
        ProfileReport
            Completed profile report.
        """

        logger.info("=" * 70)
        logger.info("Starting Dataset Profiling")
        logger.info("=" * 70)

        start_time = time.time()

        self._validate_dataset()

        self._initialize_report()

        for chunk in self._read_chunks():

            self._process_chunk(chunk)

            del chunk

            gc.collect()

        end_time = time.time()

        self.report.profiling_time_seconds = (
            end_time - start_time
        )

        logger.info("Dataset profiling completed.")

        logger.info("=" * 70)

        return self.report

    # =====================================================
    # Initialization
    # =====================================================

    def _validate_dataset(self) -> None:
        """
        Validate dataset path.
        """

        if not self.dataset_path.exists():

            logger.error(
                f"Dataset not found: {self.dataset_path}"
            )

            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        if self.dataset_path.suffix.lower() != ".csv":

            raise ValueError(
                "Profiler currently supports only CSV files."
            )

    def _initialize_report(self) -> None:
        """
        Initialize report metadata.
        """

        self.report.file_name = self.dataset_path.name

        self.report.file_size_mb = (
            self.dataset_path.stat().st_size
            / (1024 ** 2)
        )

        self.report.chunk_size = self.chunk_size

    # =====================================================
    # Read Dataset
    # =====================================================

    def _read_chunks(self):
        """
        Read dataset chunk by chunk.
        """

        logger.info(
            f"Reading dataset in chunks "
            f"of {self.chunk_size:,} rows."
        )

        return pd.read_csv(
            self.dataset_path,
            chunksize=self.chunk_size,
            low_memory=False,
        )

    # =====================================================
    # Process One Chunk
    # =====================================================

    def _process_chunk(
        self,
        chunk: pd.DataFrame,
    ) -> None:

        self._update_dataset_information(chunk)

        self._update_missing_values(chunk)

        self._update_processing_memory(chunk)

    # =====================================================
    # Dataset Information
    # =====================================================

    def _update_dataset_information(
        self,
        chunk: pd.DataFrame,
    ) -> None:
        """
        Update dataset information.
        """

        self.report.total_rows += len(chunk)

        if self.report.total_columns == 0:

            self.report.total_columns = len(chunk.columns)

            self.report.column_names = list(
                chunk.columns
            )

            self.report.data_types = {

                column: str(dtype)

                for column, dtype in chunk.dtypes.items()

            }

    # =====================================================
    # Missing Values
    # =====================================================

    def _update_missing_values(
        self,
        chunk: pd.DataFrame,
    ) -> None:
        """
        Update missing value counts.
        """

        chunk_missing = chunk.isnull().sum()

        for column, count in chunk_missing.items():

            self.report.missing_values[column] = (

                self.report.missing_values.get(
                    column,
                    0,
                )

                + int(count)

            )

    # =====================================================
    # Memory Usage
    # =====================================================

    def _update_processing_memory(
        self,
        chunk: pd.DataFrame,
    ) -> None:
        """
        Track maximum memory required to
        process one chunk.
        """

        chunk_memory = (

            chunk.memory_usage(deep=True).sum()

            / (1024 ** 2)

        )

        self.report.total_memory_mb = max(

            self.report.total_memory_mb,

            chunk_memory,

        )