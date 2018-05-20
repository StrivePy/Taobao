# Scrapy+Selenium+Chrome 抓取淘宝商品详情

## 抓取思路
由Spider发起请求（www.taobao.com)， 因为淘宝的商品详情是通过Ajax异步加载的，所以将该请求通过downloadmiddleware的**process_request**函数用selenium进行请求，并完成输入关键字并点击搜索动作，然后进入关键字商品的索引页，并将该索引页的**_response_**返回，供**index_parse**解析函数使用。索引页的**_response_**中包含了加载索引页selenium的**_Chrome_**实例和**_WebDriverWait_**实例，这两个实例供后续实现点击翻页的**next_page**函数使用。

## Scrapy模块详情

* Taobao.spiders.meishi.py

  > 爬虫模块

  * **start_request()**函数

    > 复写该函数，发起初始请求，并设置请求标志在**process_item**函数中进行过滤。在**_request_**的meta属性中设置**_brower_**和**_wait_**来接收**_Chrome_**实例和**_WebDriverWait_**实例。

  * **index_parse()**函数
   > 回调函数，用来解析经**process_request**函数处理后的索引页**_response_**，在该函数中接收**_Chrome_**实例和**_WebDriverWait_**实例。并调用翻页函数**next_page**和商品详情解析函数**product_parse**。

  * **product_parse**函数
   > 商品详情解析函数，使用**_ItemLoader_**来进行商品信息的解析。

* Taobao.middlewares.py
 > 下载中间件模块

  * **init_brower()**函数
   > 初始化**_Chrome_**实例，用**_--headless_**参数指定为无界面模式。

  * **fetch_index()**函数
   > 原始请求函数，用_**Selenium**_的**_Chrome_**请求www.baidu.com 并完成键入关键字并点击搜索的动作，然后将索引页的**_response_**返回。

  * **process_item()**函数
   > 中间件函数，复写该函数可以改变请求动作，在该函数中可以通过**_request_**的meta属性中的标志来过滤请求。在该函数中调用**fetch_index**函数来完成Ajax数据加载，并将加载完成后的数据通过**_response_**返回到**_index_parse_**回调函数中。

* Taobao.items.py
 > 项目模块

  * **ProductsItemLoader**类
   > 继承于**ItemLoader**类，用来自定义item数据的清洗动作。

  * **ProductsItem**类
   > 定义item的各个数据字段。

* Taobao.pipelines.py
 > 数据管道模块

  * **MongoPipeLine**类
   > 将抓取到的数据存储到MongoDB数据库

* Taobao.settings.py
 > 项目设置模块

  * **KEY_WORDS**
   > 设置搜索关键字

  * **MAX_PAGES**
   > 设置最大抓取页数

  * **MongoDB**参数设置
   > ```py
   > MONGO_URI = 'localhost'
   > MONGO_DB = 'computer'
   > COLLECTION = 'lianxiang'
   > ```