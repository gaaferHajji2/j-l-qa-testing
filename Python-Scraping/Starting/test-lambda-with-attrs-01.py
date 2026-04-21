import requests

from bs4 import BeautifulSoup

data = requests.get('http://www.pythonscraping.com/pages/page3.html')

bs = BeautifulSoup(data.content, 'lxml')

tags = bs.find_all(lambda tag: len(tag.attrs) >= 2 )

if tags is not None:
    for tag in tags:
        print("The Tag Is: ", tag)
else:
    print("No Tags For Condition Found")