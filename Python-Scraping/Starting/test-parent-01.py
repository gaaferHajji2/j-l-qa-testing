import requests

from bs4 import BeautifulSoup

data = requests.get('http://www.pythonscraping.com/pages/page3.html')

bs = BeautifulSoup(data.content, 'lxml')

print(bs.find('img',{'src':'../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())