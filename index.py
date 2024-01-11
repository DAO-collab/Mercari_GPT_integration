import json
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver

from utils.converttext import convert_text


class ScrapingEngine:
    def __init__(self, source_url) -> None:
        self.source_url = source_url

    def scrape_data(self):
        options = webdriver.ChromeOptions() 
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(self.source_url)
        loaded = None
        data = {}

        # Wait until the dom loads
        while loaded is None:
            dom = bs(driver.page_source, "html.parser")
            loaded = dom.find('div', attrs={'data-testid': 'price'})
            time.sleep(2)

        data['title_jp'] = convert_text(dom.find('div', attrs={'data-testid': 'name'}).div.h1.text)
        data['price_jp'] = int(dom.find('div', attrs={'data-testid': 'price'}).find_all('span')[-1].text.replace(',', ''))
        data['description_jp'] = [convert_text(dom.find('pre', attrs={'data-testid': 'description'}).text)]
        data['photos'] = []
        photos_wrapper = dom.find('div', attrs={'class', 'slick-track'}).contents
        for photo_wrapper in photos_wrapper:
            data['photos'].append(
                {
                    'path': photo_wrapper.find('img')['src']
                }
            )

        with open(file='result.txt', mode='w', encoding='utf8') as f:
            f.write(json.dumps(data,indent=4,ensure_ascii=False))

source_url = 'https://jp.mercari.com/item/m91559568533'
mercari = ScrapingEngine(source_url)
mercari.scrape_data()
