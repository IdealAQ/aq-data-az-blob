import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import sys


def setup_logging(log_level=logging.INFO, log_dir="logs"):
    log_dir = Path(log_dir)
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)-20s: %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # File handler with daily rotation (7 days history)
    file_handler = TimedRotatingFileHandler(
        log_dir / "aqblob.log", when="D", interval=1, backupCount=7, encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Root logger config
    logging.basicConfig(level=log_level, handlers=[console_handler, file_handler])
