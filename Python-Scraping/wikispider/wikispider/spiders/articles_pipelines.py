from scrapy.linkextractors import LinkExtractor

from scrapy.spiders import CrawlSpider, Rule

from scrapy.http import Response

from wikispider.items import Article

class ArticlesSpider(CrawlSpider):

    name = 'articlePipelines'

    allowed_domains = ['wikipedia.org']

    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']

    rules = [

        Rule(
            LinkExtractor(allow='(/wiki/)((?!:).)*$'),
            callback='parse_items',
            follow=True,
        ),
    ]

    def parse_items(self, response: Response):

        article = Article()

        article['url']   = response.url
        
        # print("\t\t", "-"*25)
        # print(f'The URL Is: {url}')

        article['title'] = response.css('span.mw-page-title-main::text').extract_first()
        article['text']  = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        article['last_updated'] = response.css('li#footer-info-lastmod::text').extract_first()

        return article

        # print(f'The Title Is: {title}')
        # print(f'The Text Is: {text}')
        # print(f'The Last Updated is: {last_updated}')
        # print(f"The Title Is: {title}")

        # print("\t\t", "-"*25)