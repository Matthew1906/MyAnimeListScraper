from pandas import DataFrame
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

class UserScraper(BaseScraper):
    """
    A class used to represent the User Scraper, inherits the BaseScraper.

    Methods
    -------
    scrape_from_reviews(start, end)
        Scrape users from reviews
    scrape_from_locations(locations)
        Scrape users from a list of locations
    """
    def __init__(self, path:str, filters:str):
        super().__init__(path, filters)

    def scrape_from_reviews(self, start:int, end:int)->None:
        """
        Scrape Users

        This method will loop through pages between the given parameters, 
        access each page, scrape user names and links, and save them to the CSV file.

        Parameters
        ----------
        start : int
            first page number
        end : int
            last page number + 1
        """
        link = 'https://myanimelist.net/reviews.php?t=anime&filter_check=&filter_hide=&preliminary=on&spoiler=off'
        for page in range(start, end):
            print(f"Start page {page}")
            self.driver.get(f'{link}&p={page}')
            sleep(5)
            tags = self.driver.find_elements(By.CLASS_NAME, 'username')
            print(len(tags))
            users = DataFrame.from_dict([{
                'name':tag.find_element(By.TAG_NAME, 'a').text,
                'link':tag.find_element(By.TAG_NAME, 'a').get_attribute('href'),
            } for tag in tags])
            users.to_csv(f'./data/watchlists/users{(page-1)//1000}.csv', mode="a", sep=";", header=0)
            print(f'Finish page {page}')

    def scrape_from_locations(self, locations:list)->None:
        """
        Scrape Users

        This method will loop through a list of locations, access each 
        page of users in that location, scrape user names and links, 
        and save them to the CSV file.

        Parameters
        ----------
        locations : list
            list of locations
        """
        super().init_checkpoint()
        for location in locations:
            if location in self.checkpoint['locations'] and self.checkpoint['current']!=location:
                continue
            self.start_checkpoint(location)
            start = self.checkpoint['page'] if self.checkpoint['page'] != 0 else 1
            for i in range(start, 101):
                print(f"Start location {location} page {i}")
                page = (i-1)*24
                self.driver.get(f'https://myanimelist.net/users.php?cat=user&q=&loc={location}&agelow=10&agehigh=80&g=1&show={page}')
                sleep(5)
                tags = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr td div:first-of-type a')
                users = DataFrame.from_dict([{
                    'name':tag.text,
                    'link':tag.get_attribute('href'),
                } for tag in tags]).to_csv(f'./data/watchlists/users_{location}.csv', mode="a", sep=";", header=0)
                print(f'Finish Male page {i}')
                sleep(5)
                self.driver.get(f'https://myanimelist.net/users.php?cat=user&q=&loc={location}&agelow=10&agehigh=80&g=2&show={page}')
                tags = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody tr td div:first-of-type a')
                users = DataFrame.from_dict([{
                    'name':tag.text,
                    'link':tag.get_attribute('href'),
                } for tag in tags]).to_csv(f'./data/watchlists/users_{location}.csv', mode="a", sep=";", header=0)
                print(f'Finish Female page {i}')
                print(f'Finish location {location} page {i}')
                super().increment_checkpoint(i-1)
            super().reset_checkpoint()