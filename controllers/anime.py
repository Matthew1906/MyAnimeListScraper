from selenium.webdriver.common.by import By
from time import sleep

def scrape_anime_info(driver, link:str, title:str):
    print(f"Scraping {title}")
    info = {'title':title, 'link':link}
    driver.get(link)
    sleep(4)
    left_stats = driver.find_elements(By.CSS_SELECTOR, '.spaceit_pad')
    for stat in left_stats:
        if ":" not in stat.text:
            continue
        text = stat.text.replace("\n", "")
        attr, val = text.split(":", 1)
        info[attr.strip().lower()] = val.strip()[:1+val.index(")") if ")" in val else len(val)]
    info['producers'] = list(map(lambda x:x.strip(), info['producers'].split(","))) if info.get('producers', 0)!=0 else None
    info['genres'] = list(map(lambda x:x.strip(), info['genres'].split(","))) if info.get('genres', 0)!=0 else None
    info['themes'] = list(map(lambda x:x.strip(), info['themes'].split(","))) if info.get('themes', 0)!=0 else None
    info['demographic'] = info['demographic'] if info.get('demographic', 0)!=0 else None
    # Score and Popularity
    info['score'] = driver.find_element(By.CSS_SELECTOR, '.spaceit_pad span.score-label').text 
    info['ranked'] = driver.find_element(By.CSS_SELECTOR, '.ranked strong').text
    # Streaming Platforms
    info['platforms'] = list(map(lambda x:x.text, driver.find_elements(By.CSS_SELECTOR, '.broadcast .caption')))
    info['synopsis'] = driver.find_element(By.XPATH, '//p[contains(@itemprop,"description")]').text.replace('\n', ' ')
    info['synopsis'] = info['synopsis'][:info['synopsis'].index("[")].strip() if "[]" in info['synopsis'] else info['synopsis']
    return info

def scrape_anime_characters():
    pass

def scrape_anime_staffs():
    pass

def scrape_anime_reviews():
    pass

anime_scraper = {
    'info':scrape_anime_info, 
    'character':scrape_anime_characters,
    'staff':scrape_anime_staffs,
    'review':scrape_anime_reviews
}

