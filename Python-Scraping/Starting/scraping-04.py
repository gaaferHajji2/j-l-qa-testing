import requests

from bs4 import BeautifulSoup

data = requests.get('http://www.pythonscraping.com/pages/warandpeace.html')

bs = BeautifulSoup(data.content, 'lxml')

t1 = bs.find_all('span', attrs={'class': 'green'})

t2 = bs.find_all(text='the prince')

t3 = bs.find_all(id='title')

print("The Green Span List Length is: ", len(t1))
print("The Text Content 'The Prince' List Length is: ", len(t2))
print("By Id And Class_ List Length is: ", len(t3))

for name in t1:
    print(name.get_text())