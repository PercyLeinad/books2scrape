from itemloaders.processors import TakeFirst, Compose, Identity, Join, MapCompose, SelectJmes
import scrapy
import re


def get_rating(i) -> str:
    result = re.search(r'\s+(\w*)',i)
    return result.group(1) if result else ""

class Books2Item(scrapy.Item):
    # define the fields for your item here like:
    title  = scrapy.Field(
        output_processor = TakeFirst()
    )

    price  = scrapy.Field(
        output_processor = TakeFirst()
    )

    rating = scrapy.Field(
        input_processor = MapCompose(get_rating),
        output_processor = TakeFirst()
    )
    image_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    image_urls = scrapy.Field()
