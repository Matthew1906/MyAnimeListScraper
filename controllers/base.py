from selenium.webdriver import Chrome, ChromeOptions

class BaseScraper:
    def __init__(self):
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")
        self.driver = Chrome(options=options)
        self.driver.maximize_window()