import requests

from bs4 import BeautifulSoup

data = requests.get("https://en.wikipedia.org/wiki/Kevin_Bacon")

bs = BeautifulSoup(data.content, 'lxml')

links = bs.find_all('a')

for link in links:
    if 'href' in link.attrs:
        print("The Link is: ", link)
    else:
        print(link," Doesn't has href")