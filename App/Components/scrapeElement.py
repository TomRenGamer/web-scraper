"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

"""

import logging
from bs4 import BeautifulSoup
import requests

"""
This class represents scraped element
"""


class scrapeElement:
    """
    Scrape function returns list with scraped data
    page_url - string, represents page url
    container - string, represents container which contains data (small, div, span, etc.)
    selector_type - string, represents if container has id or class
    selector_name - string, represents name of id/class
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def Scrape(self, page_url: str, container: str, selector_type: str, selector_name: str) -> list:
        try:
            self.logger.info(f"Scraping from: {page_url}")

            page_to_scrape = requests.get(page_url, timeout=10)
            page_to_scrape.raise_for_status()

            scraper = BeautifulSoup(page_to_scrape.text, "html.parser")
            scraped_texts = scraper.findAll(
                container, attrs={f"{selector_type}": f"{selector_name}"})

            if len(scraped_texts) == 0:
                raise Exception
            return scraped_texts
        except requests.exceptions.RequestException:
            self.logger.error(
                f"Request error occurred while trying to scrape: {e}")
            return []
        except requests.exceptions.Timeout:
            self.logger.error(
                f"Timeout! Try again later")
            return []
        except requests.exceptions.HTTPError as e:
            self.logger.error(
                f"HTTP Error occurred: {e}")
            return []
        except Exception as e:
            self.logger.critical(
                f"Other error occurred while trying to scrape: {e}", exc_info=True)
            return []
