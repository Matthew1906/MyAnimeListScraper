from bs4 import BeautifulSoup
from controllers import AnimeScraper
from math import ceil
from requests import get

# Globals
BASE_URL = 'https://myanimelist.net'

# Functions
get_types = lambda types:sorted([{
    'name':t.string[:t.string.index('(')-1], 
    'pages':ceil(int(t.string[t.string.index("(")+1:t.string.index(")")].replace(',', ''))/100),
    'link':BASE_URL+t['href']
} for t in types], key=lambda x:x['pages'])

# Generate anime soup
page = get(f'{BASE_URL}/anime.php')
soup = BeautifulSoup(page.text, 'html.parser')

# Get anime genres
filters = soup.select('.genre-link')
genres = [item for f in filters[:2] for item in f.select('.genre-name-link')]

# Start anime scraper
AnimeScraper(get_types(genres))