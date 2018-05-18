# -*- coding: utf-8 -*-
import scrapy
from ..items import ProductsItem, ProductsItemloader


class MeishiSpider(scrapy.Spider):
    name = 'meishi'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']

    def __init__(self, maxpage=None):
        self.maxpage = maxpage

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(
            maxpage=crawler.settings.get('MAX_PAGES')
        )

    def start_requests(self):
        base_url = 'https://www.taobao.com/'
        index_flag = {'index_flag': 'fetch index page', 'pagenumber': 1}
        yield scrapy.Request(url=base_url, callback=self.index_parse, meta=index_flag, dont_filter=True)

    def index_parse(self, response):
        product_selector = response.xpath('//div[@class="grid g-clearfix"]//div[@class="items"]/div[@data-index]')
        for selector in product_selector:
            item_loader = ProductsItemloader(item=ProductsItem(), selector=selector)
            item_loader.add_xpath('location', './/*[@class="location"]/text()')
            item_loader.add_xpath('shop_name', './/*[contains(@class, "shopname")]/span[2]/text()')
            item_loader.add_xpath('deal_count', './/*[@class="deal-cnt"]/text()')
            item_loader.add_xpath('price', './/*[contains(@class, "price")]/strong/text()')
            item_loader.add_xpath('product_brief', 'string(.//*[contains(@id, "J_Itemlist_TLink")])')
            item = item_loader.load_item()
            yield item
        next_flag = {'next_flag': 'fetch next page', 'pagenumber': response.meta['pagenumber']}
        if response.meta['pagenumber'] < self.maxpage:
            yield scrapy.Request(url=response.url, callback=self.index_parse, meta=next_flag, dont_filter=True)



