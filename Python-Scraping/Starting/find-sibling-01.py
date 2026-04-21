import requests

from bs4 import BeautifulSoup

data = requests.get('http://www.pythonscraping.com/pages/page3.html')

bs = BeautifulSoup(data.content, 'lxml')

siblings = bs.find('table', {'id': 'giftList'}).tr.next_siblings

if siblings is not None:
    for sibling in siblings:
        print(sibling)
else:
    print('No Sibling Found In Code')