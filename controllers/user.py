from pandas import DataFrame, read_csv
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

class UserScraper(BaseScraper):
    def __init__(self):
        super().__init__('users', 'clubs')
        
    def scrape_users(self, clubs:list):
        super().init_checkpoint()
        for club in clubs:
            if club['name'] in self.checkpoint['clubs'] and self.checkpoint['current']!=club['name']:
                continue
            print(f'Start club {club["name"]}')
            pages = int(ceil(club['members']/36))
            for page in range(pages):
                if club['name'] in self.checkpoint['current'] and self.checkpoint['page'] != page:
                    continue
                print(f"Start club {club['name']}, page {page+1}/{pages}")
                self.driver.get(club['link']+'&action=view&t=members&show='+str((page-1)*36))
                sleep(5)

    # pages = int(ceil(members/36))
    # showarg = (page-1)*36
    # add arguments => &action=view&t=members&show=showarg