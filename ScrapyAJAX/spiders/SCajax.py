import json
import scrapy
from ScrapyAJAX.items import ScrapyajaxItem
from scrapy.spiders import CrawlSpider, Rule


class SpidyQuotesSpider(scrapy.Spider):
    name = 'spidyquotes'
    quotes_base_url = 'http://spidyquotes.herokuapp.com/api/quotes?page=%s'
    start_urls = [quotes_base_url % 2]
    download_delay = 1.5

    def parse(self, response):
        data = json.loads(response.body)
        for items in data.get('quotes', []):
            item = ScrapyajaxItem()
            item['text'] = str(items.get('text'))
            item['author'] = str(items.get('author', {}).get('name'))
            item['tags'] = str(items.get('tags'))
            yield item

        if data['has_next']:
            next_page = data['page'] + 1
            yield scrapy.Request(self.quotes_base_url % next_page)