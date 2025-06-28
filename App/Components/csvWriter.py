"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

"""

import logging
import csv
import os


class csvWriter():
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def writeToFile(self, filename: str, data: list) -> None:
        CSV_DIR = "Csv"
        CSV_FILE = os.path.join(CSV_DIR, f"{filename}.csv")
        os.makedirs(CSV_DIR, exist_ok=True)

        try:
            with open(CSV_FILE, "w", newline="") as file:
                self.logger.info("Saving to file started")
                csvFile = csv.writer(file)
                for row in data:
                    csvFile.writerow(row)

            file.close()
            self.logger.info(f"Successfully saved data to {filename}.csv!")
        except FileExistsError:
            self.logger.error(
                "File with this name already exists!")
        except Exception as e:
            self.logger.critical(
                f"An error occurred while trying to save data to file! {e}", exc_info=True)
