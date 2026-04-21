from bs4 import BeautifulSoup as bs

import requests

data = requests.get('http://pythonscraping.com/pages/page1.html')

t1 = bs(data.content, 'html.parser')

print(t1.h1)