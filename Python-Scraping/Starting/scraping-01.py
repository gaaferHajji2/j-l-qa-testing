import requests

data = requests.get('http://pythonscraping.com/pages/page1.html')

print(data.content)