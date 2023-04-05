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
        self.recommended = '&filter_check=1&filter_hide=2%2C3'
        self.mixed_feelings = '&filter_check=2&filter_hide=1%2C3'
        self.not_recommended = '&filter_check=3&filter_hide=1%2C2'

    def scrape_reviews(self, animes:list)->None:
        super().init_checkpoint()
        for anime in animes:
            if anime['title'] in self.checkpoint['animes'] and self.checkpoint['current']!=anime['title']:
                continue
            try:
                # Start the scraping process
                print(f"Start anime {anime['title']}")
                super().start_checkpoint(anime['title'])
                if self.checkpoint['page'] < 1:
                    print(f"Scraping recommended reviews for {anime['title']}")
                    self.get_reviews(anime['title'], f"{anime['link']}/reviews?preliminary=off{self.recommended}") 
                    super().increment_checkpoint(0)
                if self.checkpoint['page']<2:
                    print(f"Scraping mixed-feelings reviews for {anime['title']}")
                    self.get_reviews(anime['title'], f"{anime['link']}/reviews?preliminary=off{self.mixed_feelings}")
                    super().increment_checkpoint(1)
                print(f"Scraping not recommended reviews for {anime['title']}")
                self.get_reviews(anime['title'], f"{anime['link']}/reviews?preliminary=off{self.not_recommended}")
                super().increment_checkpoint(2)
                print(f"Finish anime {anime['title']}")
                super().reset_checkpoint()
            except Exception:
                pass
            
    def get_reviews(self, anime:str, link:str)->None:
        self.driver.get(link)
        sleep(5)
        reviews = self.driver.find_elements(By.CLASS_NAME, 'review-element')
        DataFrame().\
        from_dict([self.get_review(review, anime) for review in reviews]).\
        to_csv(
            './data/reviews/reviews2.csv', 
            mode='a', sep=';', 
            header=0
        )
        
    def get_review(self, driver, anime:str)->dict:
        self.driver.execute_script(f"window.scrollTo(0, {driver.location['y']});")
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.readmore a').click()
        sleep(1)
        return {
            'anime':anime,
            'user':driver.find_element(By.CSS_SELECTOR, '.username a').text,
            'user_link':driver.find_element(By.CSS_SELECTOR, '.username a').get_attribute('href'),
            'rating':driver.find_element(By.CSS_SELECTOR, '.rating span').text,
            'body':driver.find_element(By.CLASS_NAME, 'text').text.replace("\n", ""),
            'status':driver.find_element(By.CLASS_NAME, 'tag').text,
        }