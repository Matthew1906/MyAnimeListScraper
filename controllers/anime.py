from pandas import DataFrame
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

class AnimeScraper(BaseScraper):
    """
    A class used to represent the Anime Scraper, inherits the BaseScraper.
    The constructor will execute the scraper and loop through each
    genres, access each page, go to the individual anime webpage, scrape all important information
    of the anime, and save them to the CSV file.

    Methods
    -------
    scrape_info(genres)
        Scrape all animes
    get_items()->list
        Get all anime titles and links in a page.
    get_info(link, title)->dict
        Retrieve all information of an anime.
    """
    def __init__(self):
        super().__init__('animes', 'genres')
        
    def scrape_info(self, genres:list)->None:
        """
        Parameters
        ----------
        genres : list
            the list of genres to scrape the animes
        """
        super().init_checkpoint()
        for genre in genres:
            # Skip a genre if it's already scraped
            if genre['name'] in self.checkpoint['genres'] and self.checkpoint['current']!=genre['name']:
                continue
            # Start the scraping process
            print(f"Start genre {genre['name']}")
            super().start_checkpoint(genre['name'])
            # Loop through each pages
            for page in range(genre['pages']):
                # Skip a page if it's already scraped
                if genre['name'] in self.checkpoint['current'] and self.checkpoint['page'] != page:
                    continue
                print(f"Start genre {genre['name']}, page {page+1}/{genre['pages']}")
                self.driver.get(f"{genre['link']}?page={page+1}")
                # Scrape anime information and save it to CSV 
                animes = DataFrame.from_dict([self.get_info(item['link'], item['name']) for item in self.get_items()])
                animes.to_csv(f'./data/animes/{"_".join(genre["name"].lower().split())}.csv', mode="a", sep=";", header=1 if page==0 else 0)
                # Update the page checkpoint
                print(f"Finish genre {genre['name']}, page {page+1}/{genre['pages']}")  
                super().increment_checkpoint(page)
                # Skip prompt
                if input('Continue?[Y]').lower() != 'y':
                    break
            if self.checkpoint['page'] != genre['pages']:
                break
            # Reset checkpoint
            print(f"Finish genre {genre['name']}")
            super().reset_checkpoint()
            # Skip prompt
            if input('Continue?[Y]').lower() != 'y':
                break

    def get_items(self)->list:
        ''' 
        Get all anime titles and links in a page and formats them into a list of dictionaries.
        
        Returns
        -------
        contents : list
            the list of dictionaries containing the anime title and link to anime page.
        '''
        sleep(5)
        contents= self.driver.find_elements(By.CSS_SELECTOR, '.seasonal-anime')
        return [{
            'name':content.find_element(By.CSS_SELECTOR, 'a.link-title').text, 
            'link':content.find_element(By.CSS_SELECTOR, 'a.link-title').get_attribute('href')
        } for content in contents]

    def get_info(self, link:str, title:str)->dict:
        '''Retrieve all information of an anime
        
        This method will go to the webpage for a single anime, wait for it
        to load, and scrape all important informations from the page.
        It will then return a dictionary of anime information to be
        stored in a CSV file. 

        Parameters
        ----------
        link : str
            URL to the individual anime page
        title : str
            Title of the Anime

        Returns
        -------
        info : dict
            anime information.
        '''
        print(f"Scraping {title}")
        info = {'title':title, 'link':link}
        self.driver.get(link)
        sleep(4)
        info['image_link'] = self.driver.find_element(By.CSS_SELECTOR, '.content img').get_attribute('src')
        left_stats = self.driver.find_elements(By.CSS_SELECTOR, '.spaceit_pad')
        for stat in left_stats:
            if ":" not in stat.text:
                continue
            text = stat.text.replace("\n", "")
            attr, val = text.split(":", 1)
            info[attr.strip().lower()] = val.strip()[:1+val.index(")") if ")" in val else len(val)]
        info['producers'] = list(map(lambda x:x.strip(), info['producers'].split(","))) if info.get('producers', 0)!=0 else None
        info['genres'] = list(map(lambda x:x.strip(), info['genres'].split(","))) if info.get('genres', 0)!=0 else None
        info['themes'] = list(map(lambda x:x.strip(), info['themes'].split(","))) if info.get('themes', 0)!=0 else None
        info['demographic'] = info['demographic'] if info.get('demographic', 0)!=0 else None
        # Score and Popularity
        info['score'] = self.driver.find_element(By.CSS_SELECTOR, '.spaceit_pad span.score-label').text 
        info['ranked'] = self.driver.find_element(By.CSS_SELECTOR, '.ranked strong').text
        # Streaming Platforms
        info['platforms'] = list(map(lambda x:x.text, self.driver.find_elements(By.CSS_SELECTOR, '.broadcast .caption')))
        # Synopsis
        info['synopsis'] = self.driver.find_element(By.XPATH, '//p[contains(@itemprop,"description")]').text.replace('\n', ' ')
        info['synopsis'] = info['synopsis'][:info['synopsis'].index("[")].strip() if "[]" in info['synopsis'] else info['synopsis']
        return info
