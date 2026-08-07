"""
profile_report.py

Purpose
-------
Stores profiling results for the dataset.

This class does NOT perform any calculations.
It only stores statistics collected by profiler.py.
"""

from dataclasses import dataclass, field


@dataclass
class ProfileReport:
    """
    Stores dataset profiling statistics.
    """

    # =====================================================
    # Dataset Information
    # =====================================================

    total_rows: int = 0

    total_columns: int = 0

    total_memory_mb: float = 0.0

    # =====================================================
    # Column Information
    # =====================================================

    column_names: list[str] = field(
        default_factory=list
    )

    data_types: dict[str, str] = field(
        default_factory=dict
    )

    missing_values: dict[str, int] = field(
        default_factory=dict
    )

    # =====================================================
    # Display Report
    # =====================================================

    def summary(self) -> None:
        """
        Print dataset profile summary.
        """

        print("\n" + "=" * 60)
        print("DATA PROFILE REPORT")
        print("=" * 60)

        print(f"Rows           : {self.total_rows:,}")

        print(f"Columns        : {self.total_columns}")

        print(
            f"Memory (MB)    : "
            f"{self.total_memory_mb:.2f}"
        )

        print("\nColumns")

        for column in self.column_names:

            dtype = self.data_types.get(column)

            missing = self.missing_values.get(column)

            print(
                f"{column:<35}"
                f"{dtype:<12}"
                f"Missing : {missing}"
            )

        print("=" * 60)