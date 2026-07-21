import logging

from src.data_engineering.config import LOG_DIR

LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = logging.FileHandler(
    LOG_DIR / "traffic_system.log"
)

console_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)