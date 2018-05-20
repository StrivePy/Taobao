# Scrapy+Selenium+Chrome 抓取淘宝商品详情

## 抓取思路

由Spider发起请求（www.taobao.com)， 因为淘宝的商品详情是通过Ajax异步加载的，所以将该请求通过downloadmiddleware的process_request函数用selenium进行请求，并完成输入关键字并点击搜索动作，然后进入关键字商品的索引页，并将该索引页的response返回，供parse解析函数使用。索引页的response中包含了加载索引页selenium的Chrome实例和WebDriverWait实例，这两个实例供后续实现点击翻页的next_page函数使用。

## Scrapy模块详情

* Taobao.spiders.meishi.py
  > 爬虫模块
  * start_request()函数
    > 复写该函数，发起初始请求，并设置请求标志在process_item函数中进行过滤
