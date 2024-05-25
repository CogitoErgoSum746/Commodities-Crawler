# items.py
import scrapy

class CommodityItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    unit = scrapy.Field()
    date = scrapy.Field()
