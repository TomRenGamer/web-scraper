"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

"""

import logging
import csv
import os

"""
Class 'csvWriter' is used to save scraped data to csv file

"""


class csvWriter():
    """
    Init function initializes saving logs from this component

    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    """
    Function writeToFile is used to write data into csv file.
    filename - string, represents name of the file
    data - list, represents list of data that will be saved to file
    """

    def writeToFile(self, filename: str, data: list) -> None:
        CSV_DIR = "Csv"
        CSV_FILE = os.path.join(CSV_DIR, f"{filename}.csv")
        os.makedirs(CSV_DIR, exist_ok=True)

        try:
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
                self.logger.info("Saving to file started")
                csvFile = csv.writer(file)
                csvFile.writerows(data)

            self.logger.info(f"Successfully saved data to {filename}.csv!")
        except FileExistsError:
            self.logger.error(
                "File with this name already exists!")
        except Exception as e:
            self.logger.critical(
                f"An error occurred while trying to save data to file! {e}", exc_info=True)
