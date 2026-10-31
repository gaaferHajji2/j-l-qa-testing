import scrapy


class EcomscraperSpider(scrapy.Spider):
    name = "ecomscraper"
    allowed_domains = ["valentino.com"]
    start_urls = ["https://www.valentino.com/en-gb/"]

    def parse(self, response):
        pass
