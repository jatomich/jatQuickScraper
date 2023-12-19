'''Description: This file creates a Scraper class that uses beautiful soup to scrape the web for text
from a url input by the user.'''
import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, url: str) -> None:
        """
        Initializes a Scraper object.

        Args:
            url (str): The URL to scrape.

        Attributes:
            url (str): The URL to scrape.
            html (str): The HTML content of the webpage.
            soup (BeautifulSoup): The BeautifulSoup object representing the parsed HTML.
            text (str): The text content extracted from the webpage.
        """
        self.url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.text = self.soup.get_text()

    def get_span_text(self) -> list:
        """
        Retrieves the text content from within the SPAN elements of a given URL.

        Returns:
            list: The text content extracted from the span tags at the URL.
        """
        span_texts = [span.get_text() for span in self.soup.find_all('span')]

        return span_texts

    def get_tag_text(self) -> list:
        """
        Retrieves the text content of HTML elements with a specified tag from a given URL.

        Returns:
            list: A list of strings containing the text content of the HTML elements.
        """
        # Prompt the user for a tag
        tag = input("Enter a tag: ")
        # Get all the text from the html
        text = self.soup.find_all(tag)
        # Return the text
        return text

    def get_text(self) -> str:
        """
        Retrieves the text content from a given URL.

        Returns:
            str: The text content extracted from the URL.
        """
        # Get all the text from the html
        text = self.soup.get_text()
        # Return the text
        return text

    def get_title(self) -> str:
        """
        Retrieves the title of a given URL.

        Returns:
            str: The title of the URL.
        """
        # Get the title from the html
        title = self.soup.title.string
        # Return the title
        return title

    def perform_scraping(self, method: int) -> str:
        # Convert the method to an int
        method: int = int(method)
        if method == 0:
            return self.get_span_text()
        elif method == 1:
            return self.get_tag_text()
        elif method == 2:
            return self.get_text()
