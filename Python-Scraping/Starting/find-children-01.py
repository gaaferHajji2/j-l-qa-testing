import requests

from bs4 import BeautifulSoup

data = requests.get('http://www.pythonscraping.com/pages/page3.html')

bs = BeautifulSoup(data.content, 'lxml')

children = bs.find('table', attrs={'id': 'giftList'}).children

if children is not None:
    for child in children:
        print(child)
else:
    print('No Items With Id=giftList')