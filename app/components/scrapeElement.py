"""
Made by TomRen
Safe scraping website: https://quotes.toscrape.com/

Simple web scraping utility.

Provides a reusable class for scraping HTML elements
based on tag name and CSS selector attributes.
"""

import logging
import requests
from bs4 import BeautifulSoup, Tag


class ScrapeElement:
    """
    Web scraper for extracting HTML elements from a webpage.

    Uses BeautifulSoup to find elements by tag name and
    a specified selector (class or id).
    """

    def __init__(self) -> None:
        """
        Initialize the scraper and configure logger.
        """
        self.logger = logging.getLogger(__name__)

    def scrape(self, page_url: str, container: str, selector_type: str, selector_name: str, elements_in_container: bool) -> list:
        """
        Scrape elements from a webpage.

        Args:
            page_url (str): URL of the page to scrape.
            container (str): HTML tag containing the data (e.g. 'div', 'span').
            selector_type (str): Selector type ('class' or 'id').
            selector_name (str): Name of the class or id.
            elements_in_container (bool): Whether the container has multiple elements.

        Returns:
            list: List of BeautifulSoup elements matching the criteria.
        """
        try:
            self.logger.info(f"Scraping from: {page_url}")

            response = requests.get(page_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            elements = soup.find_all(
                container,
                attrs={selector_type: selector_name}
            )

            if not elements:
                self.logger.warning("No elements found with given parameters")

            return elements

        except requests.exceptions.Timeout:
            self.logger.error("Request timed out")
            return []

        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            return []

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error occurred: {e}")
            return []

        except Exception as e:
            self.logger.critical(
                f"Unexpected error occurred while scraping: {e}",
                exc_info=True
            )
            return []

    @staticmethod
    def extract_text(element: Tag, elements_in_container: bool, separator: str = ", ") -> str:
        """
        Extract text from a scraped HTML element.

        Args:
            element (Tag): BeautifulSoup element to extract text from.
            elements_in_container (bool): Whether the element has multiple child elements.
            separator (str): Separator used to join texts of child elements.

        Returns:
            str: Text of the element or joined texts of its direct children.
        """
        if not elements_in_container:
            return element.get_text(" ", strip=True)

        texts = [child.get_text(" ", strip=True)
                 for child in element.find_all(recursive=False)]
        texts = [t for t in texts if t]
        return separator.join(texts) if texts else element.get_text(" ", strip=True)