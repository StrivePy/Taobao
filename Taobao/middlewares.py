# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.http import HtmlResponse
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


class TaobaoDownloaderMiddleware(object):

    def __init__(self, key_words=None):
        self.key_words = key_words
        self.brower = None
        self.wait = None
        self.time = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            key_words=crawler.settings.get('KEY_WORDS')
        )

    def init_brower(self, url):
        """
        初始化Chrome实例，设置为无窗口模式
        :param url:
        :return:
        """
        options = Options()
        options.add_argument('--headless')
        self.brower = Chrome(options=options)
        self.brower.get(url)
        self.wait = WebDriverWait(self.brower, 5)

    def fetch_index(self, request):
        """
        请求www.taobao.com，并在输入框中输入关键字联想电脑，然后点击搜索进入索引页面
        :param request:
        :return:
        """
        try:
            self.init_brower(request.url)
            keywords_inputs = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
            keywords_inputs.send_keys(self.key_words)
            submit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))
            submit_button.click()
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(request.meta['pagenumber'])))
            time.sleep(1)
            body = self.brower.page_source
            request.meta['brower'] = self.brower
            request.meta['wait'] = self.wait
            response = HtmlResponse(url=self.brower.current_url, body=body, encoding='utf-8', request=request)
            return response
        except TimeoutException:
            return None

    def process_request(self, request, spider):
        """
        通过index_flag过滤初始索引页的请求
        :param request:
        :param spider:
        :return:
        """
        if 'index_flag' in request.meta.keys():
            response = self.fetch_index(request)
            return response



