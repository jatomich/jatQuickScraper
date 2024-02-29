'''Description: This file contains the main function within which the user is prompted for a scraper method
and a url to scrape.'''
from scrapers import StarScraper, DumbScraper

def main():
    # Choose a scraper type
    scraper_choice = int(input("Select a WebScraper | 0 = StarScraper | 1 = DumbScraper |"))

    match scraper_choice:
        case 0:
            scraper = StarScraper()

            # Prompt the user for a url
            url: str = input("Enter a url: ")
            
            # Pass url to make_soup(), yielding parsed html
            soup = scraper.make_soup(url)

            # Pretty print
            print(soup.prettify())

        case 1:
            scraper = DumScraper()

            # Prompt the user to select a scraping method
            method: str = input("Enter index of desired scraping method [ { 0: 'get_span_text', 1: 'get_tag_text', 2: 'get_text' } ]: ")

            # Perform the selected scraping method
            text: str = scraper.perform_scraping(method=int(method))

            # Print the text
            print(text)


# Call the main function
if __name__ == '__main__':
    main()

