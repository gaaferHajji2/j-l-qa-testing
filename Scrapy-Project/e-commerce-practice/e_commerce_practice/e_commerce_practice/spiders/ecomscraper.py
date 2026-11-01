import scrapy
from scrapy.http import Request

class EcomscraperSpider(scrapy.Spider):
    name = "ecomscraper"
    allowed_domains = ["valentino.com"]
    start_urls = ["https://www.valentino.com/en-gb/"]

    def parse(self, response):
        categories = response.xpath("//a[@class='linkWrapper--thirdPanel']/@href").extract()
        for category in categories:
            print(f"The Extracted Category: {category}")
            print("\t\t", "="*25)

            yield Request(category, callback=self.parse_category_products)

    def parse_category_products(self, response):
        products = response.xpath("//div[@class='cardCollection__card']//a//picture//img/@data-src").extract()
        print(f"The Length Of Products is: {len(products)}")
        print("\t\t", "+"*25)
        for product in products:
            print(f"The Extracted Product Image: {product}")
            print("\t\t", "="*25)
