import scrapy
import re

from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join

from molodist.items import MolodistItem


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["molodist.store"]
    start_urls = ["https://molodist.store/shop/"]

    def parse(self, response, *kwargs):
        for link in response.css('div.product-image.scaleto a::attr(href)'):
            yield response.follow(link, self.parse_product)

        for number in range(1, 8):
            next_page = f"https://molodist.store/shop/page-{number}"
            yield response.follow(next_page, self.parse)

    def parse_product(self, response, *kwargs):
        loader = ItemLoader(item=MolodistItem(), selector=response)
        loader.default_output_processor = TakeFirst()
        price = re.findall('\d+', response.css('span.regular-price::text').get())
        loader.add_css("title", "div.products-title h1::text", MapCompose(str.strip))
        loader.add_value("price", price, Join(''))
        loader.add_css("description", "div.row.product-short-description-block p::text", Join(' '), MapCompose(str.strip))
        yield loader.load_item()
