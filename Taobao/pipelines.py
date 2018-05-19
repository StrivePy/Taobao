# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class MongoPipeline(object):
    def __init__(self, mongo_uri=None, mongo_db=None, collection=None):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection = collection
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            collection=crawler.settings.get('COLLECTION')
        )

    def open_spider(self, spider):
        self.client = MongoClient(host=self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # condition = {'shop_name': item['shop_name']}
        # self.db[self.collection].update(condition, {'$set': item}, upsert=True)
        self.db[self.collection].insert_one(dict(item))
        return item
