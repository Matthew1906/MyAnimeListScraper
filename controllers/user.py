from json import dump, load
from pandas import DataFrame
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

class UserScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.init_checkpoint()

    def init_checkpoint(self):
        try:
            with open('./data/users/checkpoint.json', 'r') as fp:
                self.checkpoint = load(fp)
        except FileNotFoundError:
            self.checkpoint = {
                'users':[], # Keep track of all scraped genres
                'current': "", # Keep track of currently being scraped genre
                'page':0 # Keep track of page
            }

    def save_checkpoint(self):
        with open('./data/users/checkpoint.json', 'w') as fp:
            dump(self.checkpoint, fp)