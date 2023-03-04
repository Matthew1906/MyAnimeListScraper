from json import dump, load
from selenium.webdriver import Chrome, ChromeOptions

class BaseScraper:
    def __init__(self, path:str, filters:str):
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        self.driver = Chrome(options=options)
        self.driver.maximize_window()
        self.path = path
        self.filters = filters

    def init_checkpoint(self):
        '''Initialize a checkpoint'''
        try:
            with open(f'./data/{self.path}/checkpoint.json', 'r') as fp:
                self.checkpoint = load(fp)
        except FileNotFoundError:
            self.checkpoint = {
                f'{self.filters}':[], # Keep track of all scraped filters
                'current': "", # Keep track of currently being scraped filter
                'page':0 # Keep track of page
            }

    def start_checkpoint(self, name:str):
        '''Start a checkpoint for a new filter'''
        self.checkpoint['current'] = name
        self.checkpoint[self.filters].append(name)
        self.checkpoint[self.filters] = list(set(self.checkpoint[self.filters]))

    def increment_checkpoint(self, page:int):
        '''Increment a page for the checkpoint (if there are any pages involved)'''
        self.checkpoint['page'] = page+1
        self.save_checkpoint()

    def reset_checkpoint(self):
        '''Reset the checkpoint'''
        self.checkpoint['current'] = ""
        self.checkpoint['page'] = 0
        self.save_checkpoint()

    def save_checkpoint(self):
        '''Save current checkpoint'''
        with open(f'./data/{self.path}/checkpoint.json', 'w') as fp:
            dump(self.checkpoint, fp)