# Description: This file uses beautiful soup to scrape the web for text from a url input by the user.

import requests
from bs4 import BeautifulSoup

def get_text(url):
    """
    Retrieves the text content from a given URL.

    Args:
        url (str): The URL to scrape the text from.

    Returns:
        str: The text content extracted from the URL.
    """
    # Get the html from the url
    html = requests.get(url).text
    # Use beautiful soup to parse the html
    soup = BeautifulSoup(html, 'html.parser')
    # Get all the text from the html
    text = soup.get_text()
    # Return the text
    return text

def get_span_text(url):
    """
    Retrieves the text content from a given URL.

    Args:
        url (str): The URL to scrape the text from.

    Returns:
        list: The text content extracted from the span tags at the URL.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    span_texts = [span.get_text() for span in soup.find_all('span')]

    return span_texts


def main():
    # Prompt the user for a url
    url = input("Enter a url: ")
    # Get the text from the url
    text = ''.join(get_span_text(url))
    # Print the text
    print(text)


# Call the main function
main()