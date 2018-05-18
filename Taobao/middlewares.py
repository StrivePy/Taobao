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
        options = Options()
        options.add_argument('--headless')
        self.brower = Chrome(options=options)
        self.brower.get(url)
        self.wait = WebDriverWait(self.brower, 5)

    def fetch_index(self, request):
        try:
            self.init_brower(request.url)
            keywords_inputs = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
            keywords_inputs.send_keys(self.key_words)
            submit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))
            submit_button.click()
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(request.meta['pagenumber'])))
            body = self.brower.page_source
            page_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
            page_box.clear()
            request.meta['pagenumber'] += 1
            page_box.send_keys(str(request.meta['pagenumber']))
            page_submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
            page_submit.click()
            time.sleep(1)
            response = HtmlResponse(url=self.brower.current_url, body=body, encoding='utf-8', request=request)
            self.brower.close()
            return response
        except TimeoutException:
            return None

    def fetch_next(self, request):
        try:
            self.init_brower(request.url)
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(request.meta['pagenumber'])))
            body = self.brower.page_source
            page_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
            page_box.clear()
            request.meta['pagenumber'] += 1
            page_box.send_keys(str(request.meta['pagenumber']))
            page_submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
            page_submit.click()
            time.sleep(1)
            response = HtmlResponse(url=self.brower.current_url, body=body, encoding='utf-8', request=request)
            self.brower.close()
            return response
        except TimeoutException:
            return None

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if 'index_flag' in request.meta.keys():
            response = self.fetch_index(request)
            return response
        elif 'next_flag' in request.meta.keys():
            response = self.fetch_next(request)
            return response


