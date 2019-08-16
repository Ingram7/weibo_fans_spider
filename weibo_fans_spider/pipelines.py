# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from pymongo import errors
from weibo_fans_spider.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME

class MongoPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.db = self.client[DB_NAME]

    def process_item(self, item, spider):
        name = type(item).__name__
        self.db[name].create_index('id')
        try:
            self.db[name].insert(dict(item))
        except errors.DuplicateKeyError:

            """
            说明有重复数据
            """
            pass
        return item

    def close_spider(self, spider):
        self.client.close()
