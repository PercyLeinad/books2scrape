import scrapy
from scrapy.loader import ItemLoader
from ..items import Books2Item
from itemloaders.processors import MapCompose

class BookSpider(scrapy.Spider):
    name = "book2"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-50.html"]

    def parse(self, response):
        for book in response.xpath('//div/ol/li'):
            item = ItemLoader(item=Books2Item(),selector=book)
            # implementing itemloader
            item.add_css('title','h3 a::text')
            item.add_css('price','p.price_color::text')
            item.add_css('rating','p[class~="star-rating"]::attr(class)')
            item.add_css('image_url','.image_container a img::attr(src)',MapCompose(lambda t: response.urljoin(t)))
            yield item.load_item()

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page),callback=self.parse)
