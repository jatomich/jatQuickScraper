'''Description: This file creates a Scraper class that uses beautiful soup to scrape the web for text
from a url input by the user.'''
from abc import ABC
import requests
from typing import Generator
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

WEBDRIVER = webdriver.Firefox()


class Scraper(ABC):
    def __init__(Scraper):
        self.webdriver = WEBDRIVER

    def make_soup():
        pass


class StarScraper(Scraper):
    '''
    Description: This class contains methods to scrape star ratings for cast members of a film or tv show.
    '''
    def __init__(self, filename: str=None, webdriver=None) -> None:
            """
            Initializes the StarScraper object.

            Args:
                filename (str, optional): The name of the file to save the scraped data. Defaults to None.
                webdriver (object, optional): The webdriver object to use for scraping. Defaults to None.

            Attributes:
                webdriver (object): The webdriver object to use for scraping.
                parser (str): The parser to use for parsing HTML content.
                base_url (str): The base URL of the web page to scrape.
                filename (str): The name of the file from which to read the tconst values.
                records (bool): A flag to indicate whether the cast dictionaries have been created.
                idx (int): An index to keep track of the current position in the data frame.
                cast_dicts (list): A list of dictionaries containing cast information.
                df (DataFrame): A pandas DataFrame containing the tconst, director, and cast columns from the Excel file.
            """
            super.__init__()

            self.parser = 'html.parser'
            self.base_url = 'https://www.imdb.com/title/'
            self.filename = filename
            self.records = False
            self.idx = 0
            self.return_to_row = None
            self.cast_dicts = None
            self.df = pd.read_excel(
                # file to read
                io=self.filename,
                # columns to incude in the data frame.
                usecols=[
                    'tconst',
                    'director',
                    'cast'
                    ],
                # spcify the data types of the columns to avoid type inference.
                dtype={
                    'tconst': str,
                    'director': str,
                    'cast': str
                    },
                # engine to use for reading the file.  We'll use openpyxl to avoid the warning message.
                engine='openpyxl'

                # uncomment the following line and comment out the previous line if you'd like to use the default engine.
                # engine=None
            )


    def make_soup(self, url: str) -> BeautifulSoup:
            """
            Retrieves the HTML content of a web page and returns it as a BeautifulSoup object.

            Args:
                url (str): The URL of the web page to scrape.

            Returns:
                BeautifulSoup: A BeautifulSoup object representing the parsed HTML content of the web page.

            Raises:
                WebDriverException: If there is an exception while retrieving the HTML content.
                TypeError: If there is a type error while processing the data.
            """
            # Open the URL in a broswer window using the webdriver object
            self.webdriver.get(url)

            # Check whether the cast dictionaries have been created
            match self.records:
                case True:
                    # Once the cast dictionaries are created, we'll flip the records flag to True, ceasing
                    # iteration through the title urls.  Instead, we'll iterate through the cast dictionaries and
                    # open the URLs of the actors in the cast list to retrieve their star ratings.
                    try:
                        # WebDriverWait will wait for the presence of the element before attempting to retrieve
                        # the outerHTML attribute, simulating more human-like behavior.
                        span = WebDriverWait(self.webdriver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME,
                                                            'starmeter-content'
                                                            ))
                        ).get_attribute('outerHTML')

                        # Return the BeautifulSoup object representing the HTML content of the web page.
                        return BeautifulSoup(
                            span,
                            self.parser
                        )
                    except WebDriverException as e:
                        print(e)
                        return None
                    except TypeError as e:
                        print(e)
                        return None

                case False:
                    # If the cast dictionaries have not been created, we'll iterate through, and open, the title URLs.
                    # We'll use the data from the title URLs to create the cast dictionaries.
                    try:
                        # WebDriverWait will wait for the presence of the element before attempting to retrieve
                        # the outerHTML attribute, simulating more human-like behavior.
                        cast = WebDriverWait(self.webdriver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME,
                                                            'ipc-metadata-list__item:last-of-type'
                                                            ))
                        ).get_attribute('outerHTML')

                        # Return the BeautifulSoup object representing the HTML content of the web page.
                        return BeautifulSoup(
                            cast,
                            self.parser
                            )
                    except WebDriverException as e:
                        print(e)
                        return None
                    except TypeError as e:
                        print(e)
                        return None


    def get_url_cast(self) -> Generator:
            """
            Retrieves the URL and cast information from the given Excel file.

            Returns:
                A generator that yields tuples of URL and cast information.

            Raises:
                AttributeError: If there is an attribute error while processing the data.
            """
            if self.return_to_row is None:
                self.return_to_row = 50

            # Generator to continually yield URL and cast information until the end of the file is reached.
            if self.df.index.size - self.return_to_row < 4:
                for idx, row in self.df.iloc[self.return_to_row:, :].iterrows():
                    print(f'self.idx: {self.idx}, self.row: {self.return_to_row}')

                    try:
                        tconst = row['tconst']
                        cast = row['cast'].split(', ')
                        url = self.base_url + tconst
                        self.return_to_row += 1

                        yield url, cast

                    except AttributeError as e:
                        print(e)
                        continue

            for idx, row in self.df.iloc[self.return_to_row:(row_num_cieling := self.return_to_row + 4), :].iterrows():
                if idx == row_num_cieling - 1:
                    self.return_to_row = row_num_cieling 
                print(f'self.idx: {self.idx}, self.row: {self.return_to_row}')

                try:
                    tconst = row['tconst']
                    cast = row['cast'].split(', ')
                    url = self.base_url + tconst

                    yield url, cast

                except AttributeError as e:
                    print(e)
                    continue


    def get_starring_links(self, soup: BeautifulSoup) -> list:
        """
        Get the links of the starring actors/actresses from the given BeautifulSoup object.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML page.

        Returns:
            list: A list of links to the starring actors/actresses.
        """
        try:
            return [link for link in soup.find(
                name='a',
                text='Stars'
                ).find_next(name='div').find_all('a')
                ]

        except AttributeError as e:
            print(e)
            return []


    def get_star_info(self, soup: BeautifulSoup=None) -> tuple:
        """
        Extracts star information from the given BeautifulSoup object.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the HTML page.

        Returns:
            tuple: A tuple containing the star rank and star count. If the star information is not found,
            returns (None, None).
        Raises:
            IndexError: If an IndexError occurs while extracting the star information.
            AttributeError: If a matching element is not found in the BeautifulSoup object.
        """
        try:
            # We'll first check whether the rating is available.  If it's not, we'll return None for both the rating
            # and the net change.
            star_string = soup.find('span', {'class': 'starmeter-current-rank'}).get_text()

            if star_string.lower() == 'see rank':
                return None, None

            # extract the star rating
            star_rating = star_string.split(' ')[1].replace(',','')

            # check whether the star rating is trending up or down
            trending = False if (trendingPath := soup.find('svg', {'class': 'ipc-icon--popularity-down'})) else True

            # extract the magnitude of the rating change
            rating_change_magnitude = trendingPath.find_all_next('span')[1].get_text() if not trending else soup.find('svg', {'class': 'ipc-icon--popularity-up'}).find_all_next('span')[1].get_text()

            # set the net change to the magnitude of the rating change if the star rating is trending up,
            # otherwise we'll set it to the negative of the magnitude of the rating change.
            net_change = rating_change_magnitude if trending else '-' + rating_change_magnitude

            return int(star_rating), int(net_change)

        # if an IndexError is raised, we'll catch it, print it to stdout, and return None for both the rating and the net change.
        except IndexError as e:
            print(e)
            return None, None
        # if a matching element is not found, we'll catch the AttributeError, print it to stdout, and return None for both the rating
        # and the net change.
        except AttributeError as e:
            print(e)
            return None, None


    def write_to_file(self, cast_dicts: list=None, filename: str='data/star_info.xlsx'):
        """
        Writes the cast dictionaries to an Excel file.

        Args:
            cast_dicts (list): A list of dictionaries containing cast information.
            filename (str): The name of the Excel file to write the data to. Default is 'data/star_info.xlsx'.

        Raises:
            NameError: If there is no data to write to the file.
        """
        try:
            pd.DataFrame(cast_dicts).to_excel(filename, index=False)
            print('Data written to file.')
        except NameError:
            print('No data to write to file.')

    
    def insert_star_data(self):
            """
            Retrieves star ratings and rating change data for actors in the cast list.
            Iterates through the cast dictionaries and opens the URLs of the actors to retrieve the data.
            Updates the cast dictionaries with the retrieved data.
            """
            # Iterate through the cast dictionaries and open the URLs of the actors to retrieve the star ratings and rating change data.
            for i, cast_dict in enumerate(self.cast_dicts[self.idx]):

                # Ensure that that we are not retrieving duplicate data.
                if cast_dict not in self.cast_dicts[self.idx:-1:-1]:

                    # Get the soup object for the URL
                    soup = self.make_soup(cast_dict['url'])

                    # If the soup object is not None, we'll retrieve the star rating and rating change data.
                    (star_rating, rating_change) = self.get_star_info(soup)
                    print(star_rating, rating_change)

                    # Update the cast dictionary at the current [self.idx][index] with the star rating and rating change data.
                    self.cast_dicts[self.idx][i].update(
                            {
                                'rating': star_rating,
                                'ratingChange': rating_change
                            }
                    )
                


    def generate_cast_dicts(self) -> None:
            """
            Generates a list of dictionaries containing information about the cast of a movie.

            Returns:
            None

            Raises:
            AttributeError: If there is an attribute error while processing the data.

            TODO: incorporate cast list from netflix data
            """
            # Iterate through the title URLs and create the cast dictionaries,
            # recording the actor's name, imdb id, URL, star rating and rating change.
            for url, _ in self.get_url_cast():
                tmpList = []
                try:
                    # Get the soup object for the URL
                    soup = self.make_soup(url)

                    # Get the links of the starring actors/actresses
                    starring_links = self.get_starring_links(soup)

                    # Iterate through the starring links and add the actor's name,
                    # imdb id, and URL to the cast_dicts list.
                    for link in starring_links:
                        # if link.get_text() not in [cast_dict['actor'] for title_cast in self.cast_dicts for cast_dict in title_cast]:
                            tmpList.append({
                                'actor': link.get_text(),
                                'nconst': link['href'].split('/')[2],
                                'url': 'https://www.imdb.com' + link['href'],
                                'rating': None,
                                'ratingChange': None
                            })

                    # Extend the cast_dicts list at the current index with the tmpList list.
                    self.cast_dicts[self.idx].extend(tmpList)

                except AttributeError as e:
                    print(e)
                    continue
                except IndexError as e:
                    print(e)
                    continue
            
            # Append a new empty list to the cast_dicts list.
            self.cast_dicts.append([])


    def scrape_star_data(self):
            """
            Scrapes star data for a movie.

            This method generates a list of dictionaries containing information about the cast of a movie.
            Each dictionary represents an actor in the cast and contains the following keys: 'actor', 'nconst', 'url', 'rating', 'ratingChange'.

            Returns:
            cast_dicts (list): A list of dictionaries representing the cast of the movie.
            """
            # If the cast_dicts list is None, we'll initialize it as a non-empty list with a dummy value
            # so that we can pass it through the loop gate below.
            if self.cast_dicts is None:
                self.cast_dicts = [[]]

            # While the length of the cast_dicts list is less than the maximum length of the data frame index,
            # we'll continue to generate cast dictionaries and insert star data in batches of 10 (set in
            # the get_url_cast method), and writing the batches to file.
            while self.idx < self.df.index.size:

                # Generate a batch of 5 cast dictionaries
                self.generate_cast_dicts()

                # Flip the records flag to True so self.get_soup() will retrieve the star rating and rating change data
                self.records = True

                # Insert star data into the cast dictionaries
                self.insert_star_data()

                # Flip the records flag to False so we can continue to iterate through the title URLs.
                self.records = False
                
                # write the cast dictionaries to file. Ultimately, we'll write the entire cast_dicts list to file.
                self.write_to_file(self.cast_dicts[self.idx],
                                    filename=f'../data/batch{self.idx}stars.xlsx')
                
                # Increment self.idx by 10, allowing access to the next batch of 10 titles.
                self.idx += 1

                # Print a message to the console indicating that a batch of 10 titles has been written.
                print('Batch of 4 titles written.')
            

            return self.cast_dicts

    
    def combine_scraped_data(self):
        """
        Combines the scraped data from batch files into a single DataFrame and saves it to a file.

        Returns:
            None
        """
        df = pd.DataFrame()

        # combine the batch files
        for file in (dirContents := os.listdir('../data')):
            if file.endswith('stars.xlsx'):
                df = pd.concat([df, pd.read_excel(f'../data/{file}')])

        # write the combined data to file
        df.to_excel('../data/CAST_LIST.xlsx', index=False)

        # remove the batch files
        for file in dirContents:
            if file.endswith('stars.xlsx'):
                os.remove(os.path.abspath(f'../data/{file}'))
    

class DumbScraper(Scraper):
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

    def make_soup(self, url: str) -> BeautifulSoup:
            """
            Retrieves the HTML content of a web page and returns it as a BeautifulSoup object.

            Args:
                url (str): The URL of the web page to scrape.

            Returns:
                BeautifulSoup: A BeautifulSoup object representing the parsed HTML content of the web page.

            Raises:
                WebDriverException: If there is an exception while retrieving the HTML content.
                TypeError: If there is a type error while processing the data.
            """
            # Open the URL in a broswer window using the webdriver object
            self.webdriver.get(url)

            try:
                # WebDriverWait will wait for the presence of the element before attempting to retrieve
                # the outerHTML attribute, simulating more human-like behavior.
                span = WebDriverWait(self.webdriver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME,
                                                    'starmeter-content'
                                                    ))
                ).get_attribute('outerHTML')

                # Return the BeautifulSoup object representing the HTML content of the web page.
                return BeautifulSoup(
                    span,
                    self.parser
                )
            except WebDriverException as e:
                print(e)
                return None
            except TypeError as e:
                print(e)
                return None

            #try:
                # WebDriverWait will wait for the presence of the element before attempting to retrieve
                # the outerHTML attribute, simulating more human-like behavior.
                #cast = WebDriverWait(self.webdriver, 10).until(
                    #EC.presence_of_element_located((By.CLASS_NAME,
                                                    #'ipc-metadata-list__item:last-of-type'
                                                    #))
                #).get_attribute('outerHTML')

                # Return the BeautifulSoup object representing the HTML content of the web page.
                #return BeautifulSoup(
                    #cast,
                    #self.parser
                    #)
            #except WebDriverException as e:
                #print(e)
                #return None
            #except TypeError as e:
                #print(e)
                #return None 
