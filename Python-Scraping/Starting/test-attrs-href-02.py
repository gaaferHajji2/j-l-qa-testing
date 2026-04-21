import requests

from bs4 import BeautifulSoup

import re

data = requests.get("https://en.wikipedia.org/wiki/Kevin_Bacon")

bs = BeautifulSoup(data.content, 'lxml')

links = bs\
.find('div', { 'id': 'bodyContent' }) \
.find_all('a', { 'href': re.compile('^(/wiki/)((?!:).)*$') })

for link in links:
    print("The HREF Of Link Is: ", link['href'])