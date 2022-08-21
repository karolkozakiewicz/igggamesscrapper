from bs4 import BeautifulSoup
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor
import time 
import ast

class Scrapper():

    def __init__(self):
        self.url = "https://igg-games.com/"
        self._url = 'https://igg-games.com/'
        self.all_content = []
        self.licznik = 1
        self.pages = 0
        self._last_url_seen = ""

    def get_content(self, url="https://igg-games.com/"):
        
        """
        Content from a whole page
        """       
        if url not in self._last_url_seen:
            print(f'Function was called: {self.licznik}/{self.pages} times.')
            self.licznik += 1
            response = requests.get(url).text
            soup = BeautifulSoup(response, features='html.parser')
            content = [link for link in [article.find('a').get('href') for article in soup.find_all('article')]]
            content_all = [link for link in [article for article in soup.find_all('article')]]

            for article in content_all:
                link = article.find('a').get('href')
                categories = [category.text for category in article.find_all('a', rel="category tag")]
                self.all_content.append([link, categories])
            self._last_url_seen = url
        time.sleep(0.2)

    def get_content_from_multiple_pages(self, pages, type='normal'):
            self.pages = pages
            pages = ['https://igg-games.com/page/{}'.format(i) for i in range(1, pages+1)]
            if type == 'normal':
                for page in pages:
                    self.get_content(url=page)
            if type == 'multi':
                with ThreadPoolExecutor(max_workers=4) as pool:
                    pool.map(self.get_content, pages)

    def save_in_file(self):
        with open(f"save-{datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.txt", 'a') as f:
            for i in self.all_content:
                f.write(str(i) + '\n')

    def get_content_by_categories(self, categories:list, type='any'):
        categories = [category.lower() for category in categories]
        output = []
        with open('list.txt', 'r') as f:
            txt_list = f.read().splitlines()
            new_txt_list = [ast.literal_eval(entry) for entry in txt_list]

        for entry in new_txt_list:
            cat = []
            for category in entry[1]:
                cat.append(category.lower())
            entry = [entry[0], cat]

            if type == 'any':
                if any(category in categories for category in entry[1]):
                    output.append(entry)

            if type == 'all':
                if all(category in entry[1] for category in categories):
                    output.append(entry)

            elif not categories:
                output.append(entry)

        with open(f"save-{'-'.join(categories)}-{type}.txt", 'a') as f:
            for i in output:
                f.write(str(i) + '\n')

    def run(self, mode='scan page'):
        if mode == 'scan page':
            scrapper.get_content_from_multiple_pages(pages=3000, type='multi')
            scrapper.save_in_file()
        if mode ==  'sort content':
            scrapper.get_content_by_categories(categories=['Adventure'], type='all')

if __name__ == "__main__":
    scrapper = Scrapper()
    scrapper.run(mode='sort content')
 






