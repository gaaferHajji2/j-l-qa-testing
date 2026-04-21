import requests

from bs4 import BeautifulSoup

def getTitle(url):
    try:
        data = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        print("\t\t", "=" * 15, f" Connection Error Check Your Internet OR URL: {url} ", "="*15)
        print("The Error Message is: ", e.__str__())
    except Exception as e1:
        print("The Error Message Is: ", e1.__str__())
    else:
        bs = BeautifulSoup(data.content, 'lxml')

        print(f"The H1-Tag Of Url {url} Is: {bs.h1} " if bs.h1 is not None else f"No Title For URL {url}")

        print("\t\t", "-" * 15)

getTitle("https://google.com")

getTitle("http://pythonscraping.com/pages/page1.html")

getTitle("https://jafar.loka")