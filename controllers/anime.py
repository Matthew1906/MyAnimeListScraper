from json import dump, load
from pandas import DataFrame
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

class AnimeScraper(BaseScraper):
    def __init__(self, genres:list):
        super().__init__()
        self.init_checkpoint()
        for genre in genres:
            if genre['name'] in self.checkpoint['genres'] and self.checkpoint['current']!=genre['name']:
                continue
            print(f"Start genre {genre['name']}")
            self.checkpoint['current'] = genre['name']
            self.checkpoint['genres'].append(genre['name'])
            self.checkpoint['genres'] = list(set(self.checkpoint['genres']))
            for page in range(genre['pages']):
                if genre['name'] in self.checkpoint['current'] and self.checkpoint['page'] != page:
                    continue
                print(f"Start genre {genre['name']}, page {page+1}")
                self.driver.get(f"{genre['link']}?page={page+1}")     
                animes = DataFrame.from_dict([self.get_info(item['link'], item['name']) for item in self.get_items()])
                animes.to_csv(f'./data/animes/{"_".join(genre["name"].lower().split())}.csv', mode="a", sep=";", header=1 if page==0 else 0)
                print(f"Finish genre {genre['name']}, page {page+1}")  
                self.checkpoint['page'] = page+1
                self.save_checkpoint()
                if input('Continue?[Y]').lower() != 'y':
                    break
            if self.checkpoint['page'] != genre['pages']:
                break
            print(f"Finish genre {genre['name']}")
            self.checkpoint['current'] = ""
            self.checkpoint['page'] = 0
            self.save_checkpoint()
            if input('Continue?[Y]').lower() != 'y':
                break
        
    def init_checkpoint(self):
        try:
            with open('./data/animes/checkpoint.json', 'r') as fp:
                self.checkpoint = load(fp)
        except FileNotFoundError:
            self.checkpoint = {
                'genres':[], # Keep track of all scraped genres
                'current': "", # Keep track of currently being scraped genre
                'page':0 # Keep track of page
            }

    def save_checkpoint(self):
        with open('./data/animes/checkpoint.json', 'w') as fp:
            dump(self.checkpoint, fp)

    def get_items(self):
        sleep(10)
        contents= self.driver.find_elements(By.CSS_SELECTOR, '.seasonal-anime')
        return [{
            'name':content.find_element(By.CSS_SELECTOR, 'a.link-title').text, 
            'link':content.find_element(By.CSS_SELECTOR, 'a.link-title').get_attribute('href')
        } for content in contents]

    def get_info(self, link:str, title:str):
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
        info['synopsis'] = self.driver.find_element(By.XPATH, '//p[contains(@itemprop,"description")]').text.replace('\n', ' ')
        info['synopsis'] = info['synopsis'][:info['synopsis'].index("[")].strip() if "[]" in info['synopsis'] else info['synopsis']
        return info

    def scrape_anime_characters():
        pass

    def scrape_anime_staffs():
        pass

    def scrape_anime_reviews():
        pass

