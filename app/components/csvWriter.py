"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

CSV file writer utility.

Provides a helper class for saving scraped data to CSV files.
"""

import logging
import csv
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

    def write_to_file(self, filename: str, data: list) -> None:
        """
        Write data to a CSV file.

        Args:
            filename (str): Name of the output file (without extension).
            data (list): Two-dimensional list representing rows of CSV data.
        """
        csv_dir = "Csv"
        csv_file = os.path.join(csv_dir, f"{filename}.csv")
        os.makedirs(csv_dir, exist_ok=True)

        try:
            self.logger.info("Saving data to CSV file started")

            with open(csv_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)

            self.logger.info(f"Successfully saved data to {filename}.csv")

        except PermissionError:
            self.logger.error("Permission denied while writing CSV file")

        except Exception as e:
            self.logger.critical(
                f"An error occurred while saving data to CSV file: {e}",
                exc_info=True
            )
