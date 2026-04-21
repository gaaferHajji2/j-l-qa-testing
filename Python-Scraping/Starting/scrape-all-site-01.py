import requests

from bs4 import BeautifulSoup

import re

pages = set()

def get_links(page_url):
    data = requests.get(f'http://en.wikipedia.org{page_url}')

    bs = BeautifulSoup(data.content, 'lxml')

    links = bs.find_all('a', { 'href': re.compile('^(/wiki/)')})

    for link in links:
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages and ':' not in link.attrs['href']:
                new_page = link.attrs['href']
                print("We Found New Page: ", link.attrs['href'])
                pages.add(new_page)

                get_links(new_page)

get_links('')