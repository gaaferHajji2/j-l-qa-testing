import scrapy
import random
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    custom_settings = {
        'LOG_FILE': 'result.log',
        'LOG_LEVEL': 'INFO'
    }

    USER_AGENTS = [
        # Chrome on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        # Chrome on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        # Firefox on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
        # Firefox on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:126.0) Gecko/20100101 Firefox/126.0",
        # Safari on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        # Chrome on Android
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        # Safari on iOS
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
        # Chrome on Linux
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        # Firefox on Linux
        "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
    ]

    def parse(self, response):
        books = response.css('article.product_pod')
        self.logger.info(f"The number of books are: {len(books)}")
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            if relative_url is not None:
                self.logger.info(f"The relative url is: {relative_url}")
                if 'catalogue/' in relative_url:
                    relative_book_url = 'https://books.toscrape.com/' + relative_url
                else:
                    relative_book_url = 'https://books.toscrape.com/catalogue/' + relative_url
                yield response.follow(
                    relative_book_url, 
                    callback=self.parse_book_page,
                    headers = { "User-Agent": self.USER_AGENTS[random.randint(0, len(self.USER_AGENTS) - 1)]}
                )
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            self.logger.info(f"The next page is: {next_page}")
            if 'catalogue/' in next_page:
                book_url = 'https://books.toscrape.com/' + next_page
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(
                book_url, 
                callback=self.parse,
                                    headers = { "User-Agent": self.USER_AGENTS[random.randint(0, len(self.USER_AGENTS) - 1)]}
            )

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