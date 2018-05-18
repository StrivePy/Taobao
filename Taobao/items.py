# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


class ProductsItemloader(ItemLoader):
    default_output_processor = TakeFirst()


class ProductsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    location = Field(
        input_processor=MapCompose(lambda x: x.replace(' ', ''))
    )
    shop_name = Field()
    deal_count = Field(
        input_processor=MapCompose(lambda x: x[0:-2])
    )
    price = Field(
        input_processor=MapCompose(lambda x: x.split('.')[0])
    )
    product_brief = Field(
        input_processor=MapCompose(str.strip)
    )

