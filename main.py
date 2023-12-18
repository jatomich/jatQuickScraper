'''Description: This file contains the main function within which the user is prompted for a scraper method
and a url to scrape.'''
from scraper import Scraper


def main():
    # Prompt the user for a url
    url = input("Enter a url: ")
    # instantiate a Scraper object
    scraper = Scraper(url=url)
    # Prompt the user for a scraper method
    method = input("Enter a scraper method [ 'get_span_text()', 'get_tag_text()', or 'get_text()' ]: ")
    # Get the text from the url
    text = ''.join(scraper[method](url))
    # Print the text
    print(text)


# Call the main function
main()

