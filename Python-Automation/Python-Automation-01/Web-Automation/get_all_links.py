import requests
from bs4 import BeautifulSoup as bs

response = requests.get('https://www.python.org/')
print(response.status_code)
assert response.status_code == 200
t1 = bs(response.content, 'lxml')
with open('links.txt', 'w', encoding='utf-8') as f:
    for link in t1.find_all('a'):
        print(f"{link} with href is: {link.get('href')}")
        f.write(f"{link} with href is: {link.get('href')}\n")