import requests

from bs4 import BeautifulSoup

from content import Content

def scrapeCNN(url) -> Content:
    data = requests.get(url)
    
    bs = BeautifulSoup(data.content, 'lxml')
    
    title = bs.find('h1').text

    body  = bs.find('div', { 'class': 'article__content' }).text

    return Content(url, title, body)

def scrapeBrookings(url) -> Content:
    data = requests.get(url)
    
    bs = BeautifulSoup(data.content, 'lxml')

    title = bs.find('h1').text

    body  = bs.find('div', { 'class': ['page', 'page-article'] }).text

    return Content(url, title, body)

url = 'https://www.brookings.edu/research/robotic-rulemaking/'
content = scrapeBrookings(url)
content.get_data()

url = 'https://www.cnn.com/2023/04/03/investing/dogecoin-elon-musk-twitter/index.html'
content = scrapeCNN(url)
content.get_data()