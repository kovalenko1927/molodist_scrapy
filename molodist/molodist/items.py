# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose

class MolodistItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(str.strip))
    price = scrapy.Field(input_processor=Join(''))
    description = scrapy.Field(input_processor=MapCompose(str.strip))
    pass
