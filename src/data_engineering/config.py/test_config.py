from pathlib import Path

# =====================================================
# Project Root Directory
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# =====================================================
# Data Directories
# =====================================================

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
MONTHLY_DATA_DIR = DATA_DIR / "monthly"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# =====================================================
# Log Directory
# =====================================================

LOG_DIR = PROJECT_ROOT / "logs"s