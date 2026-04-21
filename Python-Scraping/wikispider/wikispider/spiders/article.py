from scrapy import Request, Spider

from scrapy.http import Response

class ArticleSpider(Spider):
    name = 'article'

    def start_requests(self):
        urls = [ 
            'http://en.wikipedia.org/wiki/Python_%28programming_language%29',
            'https://en.wikipedia.org/wiki/Functional_programming',
            'https://en.wikipedia.org/wiki/Monty_Python'
        ]

        return [Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response: Response):
        url = response.url
        title = response.css('h1 span::text').extract_first()

        print("\t\t", "-"*25)
        print(f"The URL Is: {url}")
        print(f"The Title Is: {title}")
        # print(f"The Body Is: {response.text}")