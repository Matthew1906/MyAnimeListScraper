from bs4 import BeautifulSoup
from controllers import anime_scraper
from math import ceil
from json import dump, load
from pandas import DataFrame
from requests import get
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep

# Globals
BASE_URL = 'https://myanimelist.net'
CHROME_DRIVER_PATH = './chromedriver.exe'

# Generate Soup
page = get('https://myanimelist.net/anime.php')
soup = BeautifulSoup(page.text, 'html.parser')

# Get filters
filters = soup.select('.genre-link')
genres = [item for f in filters[:2] for item in f.select('.genre-name-link')]

# Functions
get_types = lambda types:[{
    'name':t.string[:t.string.index('(')-1], 
    'pages':ceil(int(t.string[t.string.index("(")+1:t.string.index(")")].replace(',', ''))/100),
    'link':BASE_URL+t['href']
} for t in types]

# Initialize Chrome Webdriver
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
driver = Chrome(options=options)
driver.maximize_window()

# Get Checkpoint
try:
    with open('./data/checkpoint.json', 'r') as fp:
        checkpoint = load(fp)
except FileNotFoundError:
    checkpoint = {
        'genres':[], # Keep track of all scraped genres
        'current': "", # Keep track of currently being scraped genre
        'page':0 # Keep track of page
    }

# Get animes
for t in get_types(genres):
    # Skip if not current genre
    if t['name'] in checkpoint['genres'] and checkpoint['current']!=t['name']:
        continue
    print(f"Start genre {t['name']}")
    checkpoint['current'] = t['name']
    checkpoint['genres'].append(t['name'])
    checkpoint['genres'] = list(set(checkpoint['genres']))
    for page in range(t['pages']):
        if t['name'] in checkpoint['current'] and checkpoint['page'] != page:
            continue
        print(f"Start genre {t['name']}, page {page+1}") 
        driver.get(f"{t['link']}?page={page+1}")
        sleep(10)
        contents= driver.find_elements(By.CSS_SELECTOR, '.seasonal-anime')
        items = [{
            'name':content.find_element(By.CSS_SELECTOR, 'a.link-title').text, 
            'link':content.find_element(By.CSS_SELECTOR, 'a.link-title').get_attribute('href')
        } for content in contents]
        animes = DataFrame.from_dict([anime_scraper['info'](driver, item['link'], item['name']) for item in items])
        animes.to_csv('./data/animes.csv', mode="a", sep=";", header=0)
        print(f"Finish genre {t['name']}, page {page+1}")  
        checkpoint['page'] = page+1
        with open('./data/checkpoint.json', 'w') as fp:
            dump(checkpoint, fp)
        if input('Continue?[Y]').lower() != 'y':
            break
    if checkpoint['page'] != t['pages']-1:
        break
    print(f"Finish genre {t['name']}")
    checkpoint['current'] = ""
    with open('./data/checkpoint.json', 'w') as fp:
        dump(checkpoint, fp)
    if input('Continue?[Y]').lower() != 'y':
        break
