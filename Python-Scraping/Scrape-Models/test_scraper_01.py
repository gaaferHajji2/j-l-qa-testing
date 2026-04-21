# from website import Website;

from crawler import Crawler

# The Old Version Of Scraper Function

class Website:
    def __init__(self, name, url, title, body):
        self.name       = name
        self.url        = url
        self.titleTag   = title
        self.bodyTag    = body

siteData = [
    ['O\'Reilly', 'https://www.oreilly.com', 'h1', 'div.title-description'],
    ['Reuters', 'https://www.reuters.com', 'h1', 'article-body__content__17Yit'],
    ['Brookings', 'https://www.brookings.edu', 'h1', 'div.page-article'],
    ['CNN', 'https://www.cnn.com', 'h1', 'div.article__content']
]

websites= []

for name, url, title, body in siteData:
    websites.append(Website(name, url, title, body))

# Here We Use Dummy Variable To Begin Work
crawler = Crawler(website=websites)

crawler.get_content(websites[0], '/library/view/web-scraping-with/9781491910283').get_data()

print("\t\t", "-"*25)

crawler.get_content(websites[1], 
        '/technology/nvidias-business-practices-eu-antitrust-spotlight-sources-say-2024-12-06/')\
    .get_data()

print("\t\t", "-"*25)

crawler.get_content(websites[2], 
        '/blog/techtank/2016/03/01/idea-to-retire-old-methods-of-policy-education/').get_data()

print("\t\t", "-"*25)

crawler.get_content(websites[3], 
        '/2023/04/03/investing/dogecoin-elon-musk-twitter/index.html').get_data()