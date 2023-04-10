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

    def scrape_from_animes(self, animes:list)->None:
        super().init_checkpoint()
        for anime in animes:
            if anime['title'] in self.checkpoint['animes'] and self.checkpoint['current']!=anime['title']:
                continue
            try:
                # Start the scraping process
                print(f"Start anime {anime['title']}")
                super().start_checkpoint(anime['title'])
                if self.checkpoint['page'] < 1:
                    res = self.get_reviews_from_anime(anime['title'], f"{anime['link']}/reviews?preliminary={anime['preliminary']}{self.recommended}") 
                    print(f"Scraped {res} recommended reviews for {anime['title']}")
                    super().increment_checkpoint(0)
                if self.checkpoint['page']<2:
                    res = self.get_reviews_from_anime(anime['title'], f"{anime['link']}/reviews?preliminary={anime['preliminary']}{self.mixed_feelings}")
                    print(f"Scraped {res} mixed-feelings reviews for {anime['title']}")
                    super().increment_checkpoint(1)
                res = self.get_reviews_from_anime(anime['title'], f"{anime['link']}/reviews?preliminary={anime['preliminary']}{self.not_recommended}")
                print(f"Scraped {res} not recommended reviews for {anime['title']}")
                super().increment_checkpoint(2)
                print(f"Finish anime {anime['title']}")
                super().reset_checkpoint()
            except Exception:
                pass
            
    def get_reviews_from_anime(self, anime:str, link:str)->None:
        self.driver.get(link)
        sleep(5)
        reviews = self.driver.find_elements(By.CLASS_NAME, 'review-element')
        DataFrame().\
        from_dict([self.get_review_from_anime(review, anime) for review in reviews]).\
        to_csv(
            './data/reviews/reviews3.csv', 
            mode='a', sep=';', 
            header=0
        )
        return len(reviews)
        
    def get_review_from_anime(self, driver, anime:str)->dict:
        self.driver.execute_script(f"window.scrollTo(0, {driver.location['y']});")
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, '.readmore a').click()
        sleep(1)
        res = {
            'anime':anime,
            'user':driver.find_element(By.CSS_SELECTOR, '.username a').text,
            'user_link':driver.find_element(By.CSS_SELECTOR, '.username a').get_attribute('href'),
            'rating':driver.find_element(By.CSS_SELECTOR, '.rating span').text,
            'body':driver.find_element(By.CLASS_NAME, 'text').text.replace("\n", ""),
            'status':driver.find_element(By.CLASS_NAME, 'tag').text,
        }
        print(f"{anime} (by {res['user']}): {res['rating']}/10")
        return res