import requests

from bs4 import BeautifulSoup

import re

data = requests.get("http://www.pythonscraping.com/pages/page3.html")

bs = BeautifulSoup(data.content, 'lxml')

images = bs.find_all('img', { 'src': re.compile('..\/img\/gifts/img.*.jpg') } )

if images is not None:
    for image in images:
        print("The Image src is: ", image['src'])
else:
    print("No Images Found")