# -*- coding: utf-8 -*-
import scrapy
import time
from ..items import ProductsItem, ProductsItemloader
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse


class MeishiSpider(scrapy.Spider):

    name = 'meishi'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']

    def __init__(self, maxpage=None, **kwargs):
        super().__init__(**kwargs)
        self.maxpage = maxpage
        self.brower = None
        self.wait = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(
            maxpage=crawler.settings.get('MAX_PAGES')
        )

    def start_requests(self):
        """
        设置brower和wait，通过request传到downloademiddleware，并通过经selenium加载处理后的索引页的response传递
        到index_parse，以供后续的翻页函数next_page使用；index_flag在process_request中过滤不同的请求
        :return:
        """
        base_url = 'https://www.taobao.com/'
        index_flag = {'index_flag': 'fetch index page', 'pagenumber': 1, 'brower': None, 'wait': None}
        yield scrapy.Request(url=base_url, callback=self.index_parse, meta=index_flag, dont_filter=True)

    def index_parse(self, response):
        """
        解析索引页的第一页，并通过第一页的HtmlResponse拿到Chrome实例和WebDriverWait实例，来实现从第二页开始翻页
        的动作。
        :param response:
        :return:
        """
        # 解析索引页的第一页
        for item in self.product_parse(response):
            yield item
        # 获取Chrome实例
        self.brower = response.meta['brower']
        # 获取WebDriverWait实例
        self.wait = response.meta['wait']
        # 从第二页开始翻页
        for page in range(2, self.maxpage):
            response = self.next_page(page)
            for item in self.product_parse(response):
                yield item

    def next_page(self, pagenumber):
        """
        实现翻页，并通过页面号码是否加载完成来判定抓取页面代码
        :param pagenumber: 页面号码，从第二页开始翻
        :return: 返回当前页的HtmlResponse实例
        """
        try:
            page_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
            page_box.clear()
            page_box.send_keys(str(pagenumber))
            page_submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
            page_submit.click()
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(pagenumber)))
            time.sleep(1)
            body = self.brower.page_source
            response = HtmlResponse(url=self.brower.current_url, body=body, encoding='utf-8')
            return response
        except TimeoutException:
            # 捕获超时异常，则回调重新加载
            self.next_page(pagenumber)

    @staticmethod
    def product_parse(response):
        """
        解析每一页的商品详情
        :param response: 每一页详情的HtmlResponse实例
        :return: 商品详情生成器
        """
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
