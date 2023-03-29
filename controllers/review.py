from pandas import DataFrame, read_csv
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

class ReviewScraper(BaseScraper):
    """
    A class used to represent the Review Scraper, inherits the BaseScraper.

    Methods
    -------
    scrape_reviews(url:str)->None
        Scrape reviews
    """
    def __init__(self):
        super().__init__('reviews', 'animes')

    def scrape_reviews(self, animes:list)->None:
        super().init_checkpoint()
        for anime in animes:
            if anime['title'] in self.checkpoint['animes'] and self.checkpoint['current']!=anime['title']:
                continue
            # Start the scraping process
            print(f"Start anime {anime['title']}")
            super().start_checkpoint(anime['title'])
            