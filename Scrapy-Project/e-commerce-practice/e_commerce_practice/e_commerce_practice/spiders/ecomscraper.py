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
        # product_urls = response.xpath("//div[@class='cardCollection__card']//a/@href").extract()
        product_images = response.xpath("//div[@class='cardCollection__card']//a//picture//img/@data-src").extract()
        print("\t\t", "+"*25)
        for product in product_images:
            print(f"The Extracted Product Image: {product}")
            print("\t\t", "="*25)
