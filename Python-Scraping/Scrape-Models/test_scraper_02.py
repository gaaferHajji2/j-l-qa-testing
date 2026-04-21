from crawler import Crawler

from website import Website

siteData = [
    ['Reuters', 'http://reuters.com', 'https://www.reuters.com/search/news?blob=',
    'div.search-result-indiv', 'h3.search-result-title a', False, 'h1', 'div.ArticleBodyWrapper'],

    ['Brookings', 'http://www.brookings.edu', 'https://www.brookings.edu/?s=',
    'div.article-info', 'h4.title a', True, 'h1', 'div.core-block']
]

sites = []

for name, url, search, rListing, rUrl, absUrl, tt, bt in siteData:
    sites.append(Website(name, url, search, rListing, rUrl, absUrl, tt, bt))

crawlers = [Crawler(site) for site in sites]
topics = ['python', 'data%20science']

for topic in topics:
    for crawler in crawlers:
        crawler.search(topic)