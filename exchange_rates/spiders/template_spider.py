import scrapy
from exchange_rates.items import CommodityItem
import re
import datetime

class TemplateSpider(scrapy.Spider):
    name = 'commodities_spider'

    def __init__(self, *args, **kwargs):
        super(TemplateSpider, self).__init__(*args, **kwargs)
        
        start_urls = ["https://markets.businessinsider.com/commodities"]

        self.start_urls = start_urls

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        # 'HTTP_PROXY': 'http://69.58.2.135:3128',
        'PROXY_POOL_ENABLED': False,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 2,   
        'LOG_LEVEL': 'DEBUG',
    }

    handle_httpstatus_list = [500, 502, 503, 504, 522, 524, 400, 403, 404, 408, 429]

    def parse(self, response):
        # print(response.request.meta.get('proxy'))
        if response.status == 200:
            # Extracting all tables and ignoring the first table
            tables = response.css('table').getall()[1:]

            for table in tables:
                # Parsing each table
                rows = scrapy.Selector(text=table).css('tbody tr')
                for row in rows:
                    item = CommodityItem()  # Create an instance of the item class

                    item['name'] = row.css('td:nth-child(1) a::text').get()
                    item['price'] = row.css('td:nth-child(2) .push-data::text').get()
                    item['unit'] = row.css('td:nth-child(5)::text').get()
                    item['date'] = row.css('td:nth-child(6) .push-data::text').get()

                    # Only yield the item if all fields are present
                    if item['name'] and item['price'] and item['unit'] and item['date']:
                        yield item

    def extract_currencies(self, url):
        parts = url.rstrip('/').split('/')
        currency_part = parts[-1]
        currencies = currency_part.split('-')

        if len(currencies) == 2:
            return currencies
        else:
            return None, None