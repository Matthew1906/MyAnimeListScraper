from bs4 import BeautifulSoup
from controllers import AnimeScraper, ReviewScraper, UserScraper, WatchlistScraper
from math import ceil
from os import remove
from pandas import read_csv
from requests import get
from os import getenv

# Globals
BASE_URL = 'https://myanimelist.net'

# Scrape animes
def get_animes()->None:
    '''
    Scrape all animes

    This function will get a list of genres using Requests.get()
    and BeautifulSoup(), then call the AnimeScraper() object
    to scrape all animes of each genres. Each genre's animes
    will be stored in a CSV file
    '''
    # Function to process retrieved genres in a helpful list format
    get_types = lambda types:sorted([{
        'name':t.string[:t.string.index('(')-1], 
        'pages':ceil(int(t.string[t.string.index("(")+1:t.string.index(")")].replace(',', ''))/100),
        'link':BASE_URL+t['href']
    } for t in types], key=lambda x:x['pages'])
    # Generate anime soup using Requests.get() and BeautifulSoup() 
    page = get(f'{BASE_URL}/anime.php')
    soup = BeautifulSoup(page.text, 'html.parser')
    # Get anime genres using soup
    filters = soup.select('.genre-link')
    genres = get_types([item for f in filters[:2] for item in f.select('.genre-name-link')])
    # Start anime scraper
    AnimeScraper().scrape_info(genres)

def get_reviews_from_animes()->None:
    '''
    Scrape reviews from animes

    This function will call the ReviewScraper() object to scrape 
    reviews from the scraped animes. This scraper will only retrieve 
    the top 'Recommended', 'Mixed Feelings', and 'Not Recommended' 
    reviews while ignoring the reviews with preliminary tag on them if
    the anime has finished airing (since preliminary means that the reviewer 
    hasn't finished the anime).
    '''
    animes = read_csv("./data/reviews/animes.csv", sep=";", index_col=0)
    ReviewScraper().scrape_from_animes(animes.to_dict('records'))

 
# page = 22
# running = True
# while running: 
#     for status in ['recommended', 'mixed_feelings', 'not_recommended']:  
#         try:
#             animes = read_csv(f"./data/reviews/{status}/{status}_{page}.csv", sep='$', index_col=0, names=['title', 'link', 'preliminary'])
#             ReviewScraper().scrape_more_reviews_from_animes(animes.to_dict('records'), status, page)
#             remove(f'./data/reviews/{status}/checkpoint.json')
#         except FileNotFoundError:
#             running = False
#             break
#     page += 1

def get_users_by_locations()->None:
    locations = ['Indonesia', 'Malaysia', 'Singapore', 'Thailand', 'Vietnam', 'Manila', 'Germany', 'France']
    UserScraper('watchlists', 'locations').scrape_from_locations(locations)

def get_watchlists()->None:
    users = read_csv("./data/watchlists/users.csv", sep=";", index_col=0)
    WatchlistScraper().get_watchlists(users.to_dict('records'))

get_watchlists()