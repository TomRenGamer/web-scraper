"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

Logging configuration for the frontend application.

Configures rotating file logging and console output
for the Flask frontend application.
"""

import logging
import sys
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "Frontend\\logs"
LOG_FILE = os.path.join(LOG_DIR, "frontend_app.log")


def setup_logging() -> None:
    """
    Configure application-wide logging.

    Sets up:
    - rotating file logs,
    - console logging to stdout,
    - unified log format,
    - reduced verbosity for external libraries.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=1_000_000,
                backupCount=3,
                encoding="utf-8"
            ),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.getLogger("urllib3").setLevel(logging.WARNING)


setup_logging()
