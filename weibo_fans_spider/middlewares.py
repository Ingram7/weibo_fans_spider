# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import pymongo
import random
from weibo_fans_spider.settings import LOCAL_MONGO_PORT, LOCAL_MONGO_HOST, DB_NAME

# cookie池
class CookiesMiddleware(object):
    """
    每次请求都随机从账号池中选择一个账号去访问
    """
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        self.account_collection = client[DB_NAME]['account']

    def process_request(self, request, spider):
        all_count = self.account_collection.find({'status': 'success'}).count()
        if all_count == 0:
            raise Exception('当前账号池为空')
        random_index = random.randint(0, all_count - 1)
        random_account = self.account_collection.find({'status': 'success'})[random_index]
        request.headers.setdefault('Cookie', random_account['cookie'])
        request.meta['account'] = random_account



# 阿布云
import base64
# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"
# 代理隧道验证信息
proxyUser = " "
proxyPass = " "
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth



from fake_useragent import UserAgent
# 随机UA
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random
