from bs4 import BeautifulSoup

import requests

try:
    data = requests.get("https://jafar.loka")
except requests.exceptions.ConnectionError as e:
    # print(type(e));
    print(e.__str__())
else:
    bs = BeautifulSoup(data.content)

    print(bs.tag1)