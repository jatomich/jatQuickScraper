'''Description: This file contains the main function within which the user is prompted for a scraper method
and a url to scrape.'''
from scraper import Scraper


def main():
    # Prompt the user for a url
    url: str = input("Enter a url: ")

    # instantiate a Scraper object
    scraper: Scraper = Scraper(url=url)

    # Prompt the user to select a scraping method
    method: str = input("Enter index of desired scraping method [ { 0: 'get_span_text', 1: 'get_tag_text', 2: 'get_text' } ]: ")

    # Perform the selected scraping method
    text: str = scraper.perform_scraping(method=int(method))

    # Get the text from the url
    #text: str = ''.join(scraper[method](url))

    # Print the text
    print(text)


# Call the main function
if __name__ == '__main__':
    main()

