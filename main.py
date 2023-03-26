from bs4 import BeautifulSoup
from controllers import AnimeScraper, ClubScraper, UserScraper
from math import ceil
from pandas import read_csv
from requests import get

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

# Scrape clubs
def get_clubs()->None:
    '''
    Scrape clubs

    This function will call the ClubScraper() object
    to scrape all clubs. All clubs will be stored in a CSV file
    '''
    ClubScraper().scrape_clubs(url=f'{BASE_URL}/clubs.php?sort=5&p=', pages=10)

# Scrape users
def get_users()->None:
    '''
    Scrape users

    This function will call the UserScraper() object
    to scrape all users on the scraped clubs. This scraper 
    will only scrape at most 1800 users (containing name and link to profile) 
    for each club.
    '''
    clubs = read_csv('./data/clubs/clubs.csv', sep=";", na_values="")
    clubs.drop(columns=clubs.columns[0], axis='columns', inplace=True)
    UserScraper().scrape_users(clubs=clubs.to_dict('records'))

get_users()
