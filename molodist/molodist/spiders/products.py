import scrapy
import re


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
        price_numbers = re.findall('\d+', response.css('span.regular-price::text').get())
        re_desc = re.sub("\s+", ' ', response.css('div.row.product-short-description-block p::text').get())
        target = {
            "title": response.css('div.products-title h1::text').get().strip(),
            "price": "".join(price_numbers),
            "description": "".join(re_desc)
        }
        yield target
