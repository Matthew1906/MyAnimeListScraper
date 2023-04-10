from math import ceil
from pandas import DataFrame
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

def clean_name(s:str)->str:
    '''Clean the filename into a valid filename format'''
    res = [l for l in s if l in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_ ']
    return "".join(res).lower().replace(' ', '_')

class UserScraper(BaseScraper):
    """
    A class used to represent the User Scraper, inherits the BaseScraper.

    Methods
    -------
    scrape_from_clubs(clubs)
        Scrape users from clubs
    """
    def __init__(self, path:str, filters:str):
        super().__init__(path, filters)
        
    def scrape_from_clubs(self, clubs:list)->None:
        """
        Scrape Users

        This method will loop through each saved clubs, access each page (max: 50 pages), 
        scrape user names and links, and save them to the CSV file.

        Parameters
        ----------
        clubs : list
            the list of clubs to scrape the animes
        """
        super().init_checkpoint()
        for club in clubs:
            if club['name'] in self.checkpoint['clubs'] and self.checkpoint['current']!=club['name']:
                continue
            print(f'Start club {club["name"]}')
            # pages = int(ceil(members/36))
            pages = int(ceil(club['members']/36))
            pages = pages if pages<=50 else 50
            super().start_checkpoint(club['name'])
            for page in range(pages):
                if club['name'] in self.checkpoint['current'] and self.checkpoint['page'] != page:
                    continue
                print(f"Start club {club['name']}, page {page+1}/{pages}")
                # showarg = (page-1)*36
                # add arguments => &action=view&t=members&show=showarg
                self.driver.get(club['link'].replace('cid','id')+'&action=view&t=members&show='+str((page)*36))
                sleep(10)
                rows = self.driver.find_elements(By.CSS_SELECTOR, 'table tbody td.borderClass')
                users = DataFrame.from_dict([{
                    'name':row.find_element(By.TAG_NAME, 'a').text,
                    'link':row.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                } for row in rows])
                print(len(users))
                users.to_csv(f'./data/clubs/users/{clean_name(club["name"])}.csv', mode="a", sep=";", header=1 if page==0 else 0)
                print(f"Finish scraping club {club['name']}, page {page+1}/{pages}")
                super().increment_checkpoint(page)
            print(f"Finish scraping {club['name']}")
            super().reset_checkpoint()
