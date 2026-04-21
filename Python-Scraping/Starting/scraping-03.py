from bs4 import BeautifulSoup

import requests

data = requests.get('http://pythonscraping.com/pages/page1.html')

t1 = BeautifulSoup(data.content, 'lxml')

print(t1.h1)