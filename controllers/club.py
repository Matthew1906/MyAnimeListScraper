from pandas import DataFrame, read_csv
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

class ClubScraper(BaseScraper):
    """
    A class used to represent the Club Scraper, inherits the BaseScraper.
    The constructor will execute the scraper and loop through each
    page and retrieve important club informations.

    Methods
    -------
    scrape_clubs(url:str, pages:int)->None
        Scrape n pages of clubs
    """
    def __init__(self):
        super().__init__('clubs')

    def scrape_clubs(self, url:str, pages:int)->None:
        ''' 
        Loop through pages of clubs and retrieve basic club data 
        to help the further scraping processes. The number of clubs 
        retrieved are (50 x pages) clubs

        Parameters
        -------
        url : str
            the link to the clubs page.
        pages: int
            number of pages to scrape club informations.
        '''
        super().init_checkpoint()
        super().start_checkpoint('clubs')
        for page in range(pages):
            # Skip a page if it's already scraped
            if self.checkpoint['page'] != page:
                continue
            self.driver.get(url+str(page+1)) 
            sleep(5)
            rows = self.driver.find_elements(By.CLASS_NAME, 'table-data')
            clubs = DataFrame.from_dict([{
                'name':row.find_element(By.CSS_SELECTOR, '.informantion a.fw-b').text,
                'link':row.find_element(By.CSS_SELECTOR, '.informantion a.fw-b').get_attribute('href'),
                'members':row.find_element(By.CSS_SELECTOR, 'td.ac').text
            } for row in rows])
            clubs.to_csv('./data/clubs/clubs.csv', mode="a", sep=";", header=1 if page==0 else 0)
            print(f"Finish scraping clubs {page+1}/{pages}")
            super().increment_checkpoint(page)
        print(f"Finish scraping {pages} pages of clubs")
        super().reset_checkpoint()
        df = read_csv('./data/clubs/clubs.csv', sep=";", na_values="",)
        df.drop(columns=df.columns[0], axis='columns', inplace=True)
        df['members'] = df['members'].str.replace(',','').astype('int32')
        df.to_csv('./data/clubs/clubs.csv', mode="w", sep=";", header=1)