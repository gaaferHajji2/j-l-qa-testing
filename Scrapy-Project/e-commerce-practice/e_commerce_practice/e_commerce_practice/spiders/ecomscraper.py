import json
import scrapy
from scrapy.http import Request
from e_commerce_practice.items import ProductItem

class EcomscraperSpider(scrapy.Spider):
    name = "ecomscraper"
    allowed_domains = ["valentino.com"]
    start_urls = ["https://www.valentino.com/en-gb/"]

    def parse(self, response):
        categories = response.xpath("//a[@class='linkWrapper--thirdPanel']/@href").extract()
        for category in categories:
            # print(f"The Extracted Category: {category}")
            # print("\t\t", "="*25)
            yield Request(category, callback=self.parse_category_products)

    def parse_category_products(self, response):
        product_urls = response.xpath("//div[@class='cardCollection__card']//a/@href").extract()
        # product_images = response.xpath("//div[@class='cardCollection__card']//a//picture//img/@data-src").extract()
        print("\t\t", "+"*25)
        for product in product_urls:
            # print(f"The Extracted Product Image: {product}")
            # print("\t\t", "="*25)
            yield Request(product, callback=self.parse_product_data)

    def parse_product_data(self, response):
        json_data_str= response.xpath('//script[contains(text(), "cif_productData")]/text()').extract()[0].split('cif_productData = "')[1].split('responseData')[0].strip()[:-2].replace('\\x22', '"')
        #print(json_data_str)
        json_data = json.loads(json_data_str)
        product_code = json_data['responseData']['sku']
        full_price = json_data['responseData']['price_range']['maximum_price']['regular_price']['value']
        price = json_data['responseData']['price_range']['maximum_price']['final_price']['value']
        currency_code = json_data['responseData']['price_range']['maximum_price']['final_price']['currency']
        product_category = json_data['responseData']['product_hierarchy'].split('/')[3]
        product_subcategory = json_data['responseData']['product_hierarchy'].split('/')[4]
        gender = json_data['responseData']['gender']
        itemurl = response.url
        image_url = json_data['responseData']['image']['responseData']['url'].replace('[image]', 'image').replace('[divArea]', '500x0')
        product_name = response.xpath('//h1[@class="pdpProductInformation__title"]/text()').extract()[0]

        item = ProductItem(
            product_code = product_code,
            full_price = full_price,
            price = price,
            currency_code = currency_code,
            country_code = 'GBR',
            item_URL = itemurl,
            image_URL = image_url,
            product_name = product_name,
            gender = gender,
            product_category = product_category,
            product_subcategory = product_subcategory
        )
        yield item
