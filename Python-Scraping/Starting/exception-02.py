from bs4 import BeautifulSoup

import requests

try:
    data = requests.get("https://google.com")
except requests.exceptions.ConnectionError as e:
    # print(type(e));
    print(e.__str__())
else:
    bs = BeautifulSoup(data.content, 'lxml')

    print("Tag Found In The Page (tag1): ", bs.tag1 is not None)