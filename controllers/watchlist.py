from datetime import datetime
from pandas import DataFrame
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper
import logging

class WatchlistScraper(BaseScraper):
    """
    A class used to represent the Watchlist Scraper, inherits the BaseScraper.

    """
    def __init__(self):
        super().__init__('watchlists', 'users')
        logging.basicConfig(
            filename='./data/watchlists/logs.txt', 
            level=logging.INFO,
            format="%(asctime)s %(message)s", 
            filemode="w"
        )
        
    def get_watchlists(self, users:dict)->None:
        super().init_checkpoint()
        for user in users:
            if user['user'] in self.checkpoint['users'] and self.checkpoint['current']!=user['user']:
                continue
            self.start_checkpoint(user['user'])
            try:
                self.driver.get(user['user_link'])
                sleep(3)
                stats = self.driver.find_elements(By.CSS_SELECTOR, 'ul.stats-status li')[:2]
                # watching = stats[0].find_element(By.TAG_NAME, 'span').text
                completed = stats[1].find_element(By.TAG_NAME, 'span').text.replace(',', '')
                # if int(watching) > 0 :
                    # watchlist.append(self.get_watchlist(user['user'], stats[0].find_element(By.TAG_NAME, 'a').get_attribute('href')))    
                status = False
                if int(completed) >0 :
                    status = self.get_watchlist(
                        username = user['user'], 
                        link = stats[1].find_element(By.TAG_NAME, 'a').get_attribute('href'),
                        length = int(completed)
                    )
                if status:
                    status = f"Added watchlist for {user['user']}, completed: {completed}"
                    print(status)
                    logging.info(status)
                else:
                    status = f"No watchlist from {user['user']}"
                    print(status)
                    logging.warning(status)
            except Exception:
                logging.error(f"Unable to get watchlist from {user['user']}")
            sleep(2)
            super().reset_checkpoint()

    def get_watchlist(self, username:str, link:str, length:int)->bool:
        sleep(5)
        self.driver.get(link)
        last_idx = 0
        while True:
            print(f"Scrolling to scrape {username}....")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(5)
            tags = self.driver.find_elements(By.CSS_SELECTOR, 'tbody.list-item tr.list-table-data')
            if len(tags) == 0 or len(tags) == last_idx:
                return False
            watchlist = [{
                'user': username,
                'anime': tag.find_element(By.CSS_SELECTOR, 'td.title a').text,
                'score': tag.find_element(By.CSS_SELECTOR, 'td.score span.score-label').text
            } for tag in tags[last_idx:]]
            DataFrame(watchlist).to_csv(
                f'./data/watchlists/watchlist_{datetime.today().strftime("%m_%d_%Y")}.csv',
                mode='a', header=0, sep=';'
            )
            last_idx = len(tags)
            if last_idx == length:
                break
        return True

