"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

CSV file writer utility.

Provides a helper class for saving scraped data to CSV files.
"""

import logging
import csv
import io
import os


class CsvWriter:
    """
    Utility class for writing tabular data to CSV files.
    """

    def __init__(self) -> None:
        """
        Initialize CSV writer and configure logger.
        """
        self.logger = logging.getLogger(__name__)

    def to_bytes(self, headers: list, rows: list) -> io.BytesIO:
        """
        Generate CSV data in memory.

        Args:
            headers (list): Column headers written as the first row.
            rows (list): Two-dimensional list representing rows of CSV data.

        Returns:
            io.BytesIO: CSV file encoded in UTF-8 with BOM, ready for send_file.
        """
        text = io.StringIO()
        writer = csv.writer(text)
        writer.writerow(headers)
        writer.writerows(rows)

        return io.BytesIO(text.getvalue().encode("utf-8-sig"))