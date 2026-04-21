from scrapy.linkextractors import LinkExtractor

from scrapy.spiders import CrawlSpider, Rule

from scrapy.http import Response

class ArticlesSpider(CrawlSpider):

    name = 'articles'

    allowed_domains = ['wikipedia.org']

    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']

    rules = [

        Rule(
            LinkExtractor(allow='(/wiki/)((?!:).)*$'),
            callback='parse_items',
            follow=True,
            cb_kwargs={'is_article': True}
        ),

        Rule(
            LinkExtractor(allow=r'.*',),
            callback='parse_items',
            # follow=True,
            cb_kwargs={'is_article': False}
        ),
    ]

    def parse_items(self, response: Response, is_article: bool):
        url   = response.url
        
        print("\t\t", "-"*25)
        print(f'The URL Is: {url}')

        title = response.css('span.mw-page-title-main::text').extract_first()

        if is_article:
            text  = response.xpath('//div[@id="mw-content-text"]//text()').extract()
            last_updated = response.css('li#footer-info-lastmod::text').extract_first()

            print(f'The Title Is: {title}')
            print(f'The Text Is: {text}')
            print(f'The Last Updated is: {last_updated}')
        else:
            print(f"The Title Is: {title}")

        print("\t\t", "-"*25)