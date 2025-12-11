"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

"""

import logging
import sys
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "Logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

"""
Function setup_logging is used to save logs while app works

"""


def setup_logging() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=1e6,
                backupCount=3,
                encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ])

    logging.getLogger("urllib3").setLevel(logging.WARNING)


setup_logging()
