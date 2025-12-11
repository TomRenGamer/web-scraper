"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

"""

from Components.scrapeElement import scrapeElement
from Components.csvWriter import csvWriter
import logging
import sys

"""
Class App represents scraper application and implements all components
"""


class App:
    """
    Init functions implements scrapeElement component and logs object
    """

    def __init__(self) -> None:
        self.app = scrapeElement()
        self.scraped_elements = list()
        self.matched_elements = list()
        self.csv_writer = csvWriter()
        self.logger = logging.getLogger(__name__)

    """
    Run function starts whole application
    """

    def run(self) -> None:
        try:
            self.logger.info(f"Started app")
            try:
                number_of_scraping = int(
                    input("Enter amount of data to scrape: "))
                self.logger.debug(
                    f"User entered amount of data to scrape: {number_of_scraping}")
            except ValueError:
                self.logger.error(
                    "Invalid input for scraping count (not an integer)")
            except Exception as e:
                self.logger.critical(f"Other error: {e}", exc_info=True)

            page_url = str(input("Enter website url: "))
            self.logger.debug(f"User entered page url: {page_url}")

            for i in range(number_of_scraping):
                try:
                    container = str(input("Enter container containing data: "))
                    selector_type = input(
                        "Does your container have class or id? (Type 'class' or 'id'): ").strip()
                    selector_name = str(input("Enter name of class/id: "))

                    self.logger.debug(
                        f"Scraping params: page_url: {page_url}, container: {container}, selector_type: {selector_type}, selector_name: {selector_name}")
                    temp = self.app.Scrape(
                        page_url, container, selector_type, selector_name)
                    self.scraped_elements.append(
                        [element.text.strip() for element in temp])
                except ValueError:
                    self.logger.error(f"Value must be an string!")
                except Exception as e:
                    self.logger.critical(f"Other error: {e}", exc_info=True)

            if number_of_scraping >= 2:
                for index, paired_elements in enumerate(zip(*self.scraped_elements), start=1):
                    print(f"{index}. " + " - ".join(paired_elements))
                    self.matched_elements.append(
                        "-|*- ".join(paired_elements).split("-|*-"))
            else:
                for index, element in enumerate(self.scraped_elements[0], start=1):
                    print(f"{index}. {element}")
                    self.matched_elements.append(element)

            self.logger.info("Scraping completed successfully!")

            try:
                filesave = str(
                    input("Would You like to save scraped data to csv file? (Y/N) ")).strip().upper()

                if filesave == "Y":
                    headings = str(
                        input("Enter headings of data separated with commas: ")).strip().split(",")

                    self.matched_elements.insert(0, headings)

                    filename = str(input("Enter name of csv file: ")).strip()
                    self.csv_writer.writeToFile(
                        filename, self.matched_elements)
                else:
                    sys.exit()
            except ValueError:
                self.logger.error(f"Value must be an string 'Y' or 'N'!")
            except Exception as e:
                self.logger.critical(
                    f"Other error occurred: {e}", exc_info=True)
        except Exception as e:
            self.logger.critical(f"Other error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    my_app = App()
    my_app.run()