import requests

from bs4 import BeautifulSoup

import re

pages = set()

def get_links(page_url):
    data = requests.get(f'http://en.wikipedia.org{page_url}', allow_redirects=True)
    bs = BeautifulSoup(data.content, 'lxml')

    try:
        print("The H1-Text Is: ", bs.h1.get_text())
        print("\t\t", "*" * 20)
        
        t1 = bs.find(id='mw-content-text').find('p')
        print("The First P Is: ", t1)
        print("\t\t", "/" * 20)

        # t2 = bs.find(id= 'ca-edit').find('span').find('a').attrs['href'];
        # print("The HREF-Data Is: ", t2);
    
        # print("\t\t", "+" * 20);

    except AttributeError as e: 
        print("We Don't Have Data, With Error: ", e.__str__())

        # return [];
    except Exception as ex:
        print("We Have General Error: ", ex.__str__())
        # return [];

    links = bs.find_all('a', { 'href': re.compile('^(/wiki/)')})

    for link in links:
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages and ':' not in link.attrs['href']:
                new_page = link.attrs['href']

                print("We Have New Page: ", new_page)

                print("\t\t", "-" * 20)

                pages.add(new_page)

                get_links(new_page)

get_links('')