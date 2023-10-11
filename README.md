# AnimeListScraper

This is a web scraper made using [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) and [Selenium](https://pypi.org/project/selenium/) to scrape [MyAnimeList](https://myanimelist.net/) website.

This project uses [Chrome webdriver](https://chromedriver.chromium.org/) to automate the scraping process. 

The resulting scraping data is saved in semicolon delimited [CSV](https://www.businessinsider.com/guides/tech/what-is-csv-file) files and are still [dirty](https://www.techopedia.com/definition/1194/dirty-data).

I wouldn't recommend running the scraper since it takes quite a while to retrieve the data. 

You can just get the data (in [JSON](https://www.educba.com/json-vs-csv/#:~:text=JSON%20is%20referred%20to%20as,small%20files%20and%20fewer%20data.) format) by running the code inside this [Google Colab](https://colab.research.google.com/drive/1WYLwb-q6NTjlSnnyIFSgaf3vbpovqEO8?usp=sharing). I've removed the duplicates, but there are some empty values that I didn't handle. Or you can also simply clone this repository and download the raw CSV anime and review data. As for watchlists, you can access the scraping result in this [Google Drive](https://drive.google.com/drive/folders/1uioZ9KMeWGwzJORDAJPpo_WCoQDMTq2E) folder.

## Languages and Technologies:
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
