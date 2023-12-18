'''Description: This file creates a Scraper class that uses beautiful soup to scrape the web for text
from a url input by the user.'''
import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, url):
        self.url = url
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.text = self.soup.get_text()
    
    def get_span_text(self):
        """
        Retrieves the text content from within the SPAN elements of a given URL.

        Args:
            url (str): The URL to scrape the text from.

        Returns:
            list: The text content extracted from the span tags at the URL.
        """
        span_texts = [span.get_text() for span in self.soup.find_all('span')]

        return span_texts

    def get_tag_text(self):
        """
        Retrieves the text content of HTML elements with a specified tag from a given URL.

        Args:
            url (str): The URL of the webpage to scrape.

        Returns:
            list: A list of strings containing the text content of the HTML elements.

        """
        # Prompt the user for a tag
        tag = input("Enter a tag: ")
        # Get all the text from the html
        text = self.soup.find_all(tag)
        # Return the text
        return text

    def get_text(self):
        """
        Retrieves the text content from a given URL.

        Args:
            url (str): The URL to scrape the text from.

        Returns:
            str: The text content extracted from the URL.
        """
        # Get all the text from the html
        text = self.soup.get_text()
        # Return the text
        return text