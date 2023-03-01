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
        try:
            with open(f'./data/{self.path}/checkpoint.json', 'r') as fp:
                self.checkpoint = load(fp)
        except FileNotFoundError:
            self.checkpoint = {
                f'{self.filters}':[], # Keep track of all scraped genres
                'current': "", # Keep track of currently being scraped genre
                'page':0 # Keep track of page
            }

    def restart_checkpoint(self, name:str):
        self.checkpoint['current'] = name
        self.checkpoint[self.filters].append(name)
        self.checkpoint[self.filters] = list(set(self.checkpoint[self.filters]))

    def increment_checkpoint(self):
        self.checkpoint['page'] = page+1
        self.save_checkpoint()

    def reset_checkpoint(self):
        self.checkpoint['current'] = ""
        self.checkpoint['page'] = 0
        self.save_checkpoint()

    def save_checkpoint(self):
        with open(f'./data/{self.path}/checkpoint.json', 'w') as fp:
            dump(self.checkpoint, fp)