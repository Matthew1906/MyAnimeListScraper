from json import dump, load
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class BaseScraper:
    """
    A class used to represent the Base Scraper. 
    
    This class contains the initialization of the Selenium Webdriver 
    and methods related to the checkpoint system used to keep track 
    of scraped items.

    Attributes
    ----------
    drive : ChromeDriver
        the webdriver to move around the web using Selenium.
    path : str
        the folder name to save the scraping results and the type of data you are currently scraping.
    filters : str
        the filter name for the checkpoint.
    checkpoint : dict
        the dictionary object to store the current scraping progress.
    
    Methods
    -------
    init_checkpoint()
        Initializes the checkpoint for the scraper.
    
    start_checkpoint(name)
        Updates the checkpoint current filter.
    
    increment_checkpoint(page)
        Increment the page value for the checkpoint.
    
    reset_checkpoint()
        Reset the current value when the scraping of a certain filter is completed.
    
    save_checkpoint()
        Saves the current checkpoint.

    """
    def __init__(self, path:str, filters:str="filters"):
        """
        Parameters
        ----------
        path : str
            the folder name to save the scraping results
        filters : str
            the filter name for the checkpoint
        """
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage') 
        self.driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()
        self.path = path
        self.filters = filters

    def init_checkpoint(self)->None:
        '''Initializes the checkpoint for the scraper
        
        This method will check if a checkpoint file already exists.
        If a checkpoint file already exists, it will simply load them
        using json.load(). If it doesn't, create a new dictionary.
        '''
        try:
            with open(f'./data/{self.path}/checkpoint.json', 'r') as fp:
                self.checkpoint = load(fp)
        except FileNotFoundError:
            self.checkpoint = {
                f'{self.filters}':[], # Keep track of all scraped filters
                'current': "", # Keep track of currently being scraped filter
                'page':0 # Keep track of page
            }

    def start_checkpoint(self, name:str)->None:
        '''Updates the checkpoint current filter
        
        This method will update the 'current' key on the checkpoint
        to show that a certain filter is currently being scraped.
        This method will also add the filter name into the list
        of filters. This list stores all scraped filters.

        Parameters
        ----------
        name : str
            the filter name to update the current filter in checkpoint 
        '''
        self.checkpoint['current'] = name
        self.checkpoint[self.filters].append(name)
        # Use set() to make sure that the filters are all unique
        self.checkpoint[self.filters] = list(set(self.checkpoint[self.filters]))

    def increment_checkpoint(self, page:int)->None:
        '''Increment the page value for the checkpoint
        
        This method will increment the page for the checkpoint, so that
        when the user starts the scraper, it will just scrape the next page

        Parameters
        ----------
        page : int
            the page number (starts from 0)
        '''
        self.checkpoint['page'] = page+1
        self.save_checkpoint()

    def reset_checkpoint(self)->None:
        '''Reset the current value when the scraping of a certain filter is completed'''
        self.checkpoint['current'] = ""
        self.checkpoint['page'] = 0
        self.save_checkpoint()

    def save_checkpoint(self)->None:
        '''Save current checkpoint
        
        This method will save the checkpoint to the folder based on 
        the path value. This value basically tells you the type of 
        things you are currently scraping.
        '''
        with open(f'./data/{self.path}/checkpoint.json', 'w') as fp:
            dump(self.checkpoint, fp, indent=4)