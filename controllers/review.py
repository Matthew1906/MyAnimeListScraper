from json import dump, load
from pandas import DataFrame
from selenium.webdriver.common.by import By
from time import sleep
from .base import BaseScraper

class ReviewScraper(BaseScraper):
    def __init__(self):
        super().__init__()