import scrapy

from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join

from molodist.items import MolodistItem


class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ["molodist.store"]
    start_urls = ["https://molodist.store/shop/"]

    def parse(self, response, *kwargs):
        for number in range(1, 8):
            next_page = f"https://molodist.store/shop/page-{number}"
            yield response.follow(next_page, self.parse_full_link)

    def parse_full_link(self, response):
        for link in response.css('div.product-image.scaleto a::attr(href)'):
            yield response.follow(link, self.parse_product)

    def parse_product(self, response, *kwargs):
        loader = ItemLoader(item=MolodistItem(), selector=response)
        loader.default_output_processor = TakeFirst()
        loader.add_css("title", "div.products-title h1::text")
        loader.add_css("price", 'span.regular-price::text', re='\d+')
        loader.add_css("description", "div.row.product-short-description-block p::text")
        yield loader.load_item()
