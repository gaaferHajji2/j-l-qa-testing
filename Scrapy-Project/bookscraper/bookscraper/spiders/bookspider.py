import scrapy

from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    custom_settings = {
        'LOG_FILE': 'result.log',
        'LOG_LEVEL': 'INFO'
    }

    def parse(self, response):
        books = response.css('article.product_pod')
        self.logger.info(f"The number of books are: {len(books)}")
        for book in books:
            relative_url = response.css('h3 a ::attr(href)').get()
            if relative_url is not None:
                self.logger.info(f"The relative url is: {relative_url}")
                if 'catalogue/' in relative_url:
                    book_url = 'https://books.toscrape.com/' + relative_url
                else:
                    book_url = 'https://books.toscrape.com/catalogue/' + relative_url
                yield response.follow(book_url, callback=self.parse_book_page)
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            self.logger.info(f"The next page is: {next_page}")
            if 'catalogue/' in next_page:
                book_url = 'https://books.toscrape.com/' + next_page
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(book_url, callback=self.parse)

    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        item = BookItem()
        item['url'] = response.url
        item['title'] = response.css('.product_main h1::text').get()
        item['product_type'] = table_rows[1].css('td::text').get()
        item['price_excl_tax'] = table_rows[2].css('td::text').get()
        item['price_incl_tax'] = table_rows[3].css('td::text').get()
        item['tax'] = table_rows[4].css('td::text').get()
        item['availability'] = table_rows[5].css('td::text').get()
        item['num_reviews'] = table_rows[6].css('td::text').get()
        item['stars'] = response.css("p.star-rating").attrib['class']
        item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        item['price'] = response.css('p.price_color::text').get()
        yield item