# -*- coding: utf-8 -*-

from scrapy import cmdline

spider_name = 'meishi'
cmd = 'scrapy crawl {spider_name}'.format(spider_name=spider_name)
cmdline.execute(cmd.split())
