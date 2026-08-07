"""
profile_report.py

Purpose
-------
Defines the ProfileReport class, which stores all statistics
generated during dataset profiling.

Responsibilities
----------------
- Store profiling results.
- Provide a structured object for profiler.py.
- Contain NO business logic.
- Contain NO pandas code.
- Contain NO file reading.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ProfileReport:
    """
    Stores all profiling statistics for a dataset.

    This class acts only as a data container.
    It does not calculate any statistics.
    """

    # ==========================================================
    # Dataset Information
    # ==========================================================

    total_rows: int = 0

    total_columns: int = 0

    total_memory_mb: float = 0.0

    # ==========================================================
    # Column Information
    # ==========================================================

    column_names: List[str] = field(
        default_factory=list
    )

    data_types: Dict[str, str] = field(
        default_factory=dict
    )

    # ==========================================================
    # Data Quality
    # ==========================================================

    missing_values: Dict[str, int] = field(
        default_factory=dict
    )

    duplicate_rows: int = 0

    # ==========================================================
    # Column Statistics
    # ==========================================================

    unique_values: Dict[str, int] = field(
        default_factory=dict
    )

    minimum_values: Dict[str, float] = field(
        default_factory=dict
    )

    maximum_values: Dict[str, float] = field(
        default_factory=dict
    )

    mean_values: Dict[str, float] = field(
        default_factory=dict
    )

    median_values: Dict[str, float] = field(
        default_factory=dict
    )

    std_values: Dict[str, float] = field(
        default_factory=dict
    )

    # ==========================================================
    # Time Information
    # ==========================================================

    start_date: Optional[str] = None

    end_date: Optional[str] = None

    start_time: Optional[str] = None

    end_time: Optional[str] = None

    # ==========================================================
    # Metadata
    # ==========================================================

    file_name: str = ""

    file_size_mb: float = 0.0

    profiling_time_seconds: float = 0.0

    chunk_size: int = 0