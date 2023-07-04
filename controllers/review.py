from datetime import datetime
from pandas import DataFrame, read_csv
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

class ReviewScraper(BaseScraper):
    """
    A class used to represent the Review Scraper, inherits the BaseScraper.

    Methods
    -------
    scrape_from_animes(animes:list)->None
        Scrape reviews from animes
    scrape_more_reviews_from_animes(animes:list, rec:str, page:int)->None
        Scrape the next pages of anime reviews
    get_reviews_from_anime(self, anime:str, link:str)->None:
        Get the reviews from the visited page and save them into a file
    get_review_from_anime(self, driver, anime:str)->dict:
        Get review data from the HTML tag and return a dictionary of review data    
    """
    def __init__(self):
        super().__init__('reviews', 'animes')
        self.recommended = '&filter_check=1&filter_hide=2%2C3'
        self.mixed_feelings = '&filter_check=2&filter_hide=1%2C3'
        self.not_recommended = '&filter_check=3&filter_hide=1%2C2'

    def scrape_from_animes(self, animes:list)->None:
        '''Scrape reviews from animes
        
        This method will loop each anime page three times to get all 
        three types of reviews (recommended, mixed feelings, not recommended)

        Parameters
        ----------
        animes : list
            list of dictionaries containing anime name and link to the anime page
        '''
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
    
    def scrape_more_reviews_from_animes(self, animes:list, rec:str, page:int)->None:
        '''Scrape the next pages of anime reviews
        
        This method will scrape even more reviews from a list of animes.
        The animes are selected based on the number of previously
        scraped reviews of that anime. If there are 20 reviews, I 
        assumed that there are more (since the limit per page is
        20 reviews)

        Parameters
        ----------
        animes : list
            list of dictionaries containing anime name and link to the anime page
        rec : str
            label of the reviews (recommended, mixed feelings, not recommended)
        page : int
            page number of the review page
        '''
        self.path = f'reviews/{rec}'
        super().init_checkpoint()
        arg = {
            'recommended':self.recommended,
            'mixed_feelings':self.mixed_feelings,
            'not_recommended':self.not_recommended
        }
        for anime in animes:
            if anime['title'] in self.checkpoint['animes'] and self.checkpoint['current']!=anime['title']:
                continue
            try:
                # Start the scraping process
                self.start_checkpoint(anime['title'])
                res = self.get_reviews_from_anime(
                    anime['title'], 
                    f"{anime['link']}/reviews?preliminary={anime['preliminary']}{arg[rec]}&p={page}"
                )
                if res >=20 :
                    DataFrame(data=[anime]).to_csv(f'./data/reviews/{rec}/{rec}_{page+1}.csv', mode='a', sep='$', header=0)
                print(f"Scraped {res} {rec} reviews for {anime['title']} page {page}")
                self.reset_checkpoint()
            except Exception:
                pass            

    def get_reviews_from_anime(self, anime:str, link:str)->None:
        '''Get the reviews from the visited page and save them into a file
        
        This method will visit the anime link and get the information 
        of each HTML tags containing the review information. 
        The method will then call another function to get the review 
        and store them into a CSV file.

        Parameters
        ----------
        anime : str
            title of the anime
        link : str
            URL to the individual anime page
        '''
        self.driver.get(link)
        sleep(5)
        reviews = self.driver.find_elements(By.CLASS_NAME, 'review-element')
        DataFrame().\
        from_dict([self.get_review_from_anime(review, anime) for review in reviews]).\
        to_csv(
            f'./data/reviews/reviews_{datetime.today().strftime("%m_%d_%Y")}.csv', 
            mode='a', sep=';', 
            header=0
        )
        return len(reviews)
        
    def get_review_from_anime(self, driver, anime:str)->dict:
        '''Get review data from the HTML tag and return a dictionary of review data 
        
        This method will scroll the page into the location of the HTML 
        tag and scrape all necessary anime review information

        Parameters
        ----------
        driver : WebElement
            instance of the review element
        anime : str
            anime title

        Returns
        -------
        info : dict
            review information
        '''
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