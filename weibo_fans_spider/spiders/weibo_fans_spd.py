# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from ..items import WeiboFansSpiderItem


class WeiboFansSpdSpider(scrapy.Spider):
    name = 'weibo_fans_spd'

    start_urls = ['https://m.weibo.cn/api/container/getIndex?containerid=1076031223178222&page={}'
                      .format(i) for i in range(1, 376)]
    repost_url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'
    comment_url = 'https://m.weibo.cn/api/comments/show?id={}&page={}'
    attitudes_url = 'https://m.weibo.cn/api/attitudes/show?id={}&page={}'
    user_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}'

    def parse(self, response):
        data = json.loads(response.text)
        if data.get('ok') == 1:
            weibos = data.get('data').get('cards')
            for weibo in weibos:
                mblog = weibo.get('mblog')

                if mblog:
                    mid = mblog.get('mid')

                    # 转发
                    yield scrapy.Request(self.repost_url.format(mid, 1), callback=self.parse_repost, meta={'mid': mid, 'page': 1})

                    # 评论
                    yield scrapy.Request(self.comment_url.format(mid, 1), callback=self.parse_comment, meta={'mid': mid, 'page': 1})

                    # 点赞
                    yield scrapy.Request(self.attitudes_url.format(mid, 1), callback=self.parse_attitudes, meta={'mid': mid, 'page': 1})


    # 转发
    def parse_repost(self, response):
        data = json.loads(response.text)
        if data['ok'] == 1:
            for i in data.get('data').get('data'):
                item = WeiboFansSpiderItem()
                item['id'] = i.get('user').get('id')
                item['statuses_count'] = i.get('user').get('statuses_count')
                item['screen_name'] = i.get('user').get('screen_name')
                item['profile_url'] = i.get('user').get('profile_url')
                item['description'] = i.get('user').get('description')
                item['gender'] = i.get('user').get('gender')
                item['followers_count'] = i.get('user').get('followers_count')
                item['follow_count'] = i.get('user').get('follow_count')
                yield item
            mid = response.meta['mid']
            page = response.meta['page'] + 1
            yield Request(self.repost_url.format(mid, page),
                          callback=self.parse_repost, meta={'page': page, 'mid': mid})
    # 评论
    def parse_comment(self, response):
        data = json.loads(response.text)
        if data['ok'] == 1:
            for i in data.get('data').get('data'):
                id = i.get('user').get('id')
                yield Request(self.user_url.format(id), callback=self.parse_user)

            mid = response.meta['mid']
            page = response.meta['page'] + 1
            yield Request(self.comment_url.format(mid, page),
                          callback=self.parse_comment, meta={'page': page, 'mid': mid})


    # 点赞
    def parse_attitudes(self, response):
        data = json.loads(response.text)
        if data['ok'] == 1:
            for i in data.get('data').get('data'):
                id = i.get('user').get('id')
                yield Request(self.user_url.format(id), callback=self.parse_user)

            mid = response.meta['mid']
            page = response.meta['page'] + 1
            yield Request(self.attitudes_url.format(mid, page),
                          callback=self.parse_attitudes, meta={'page': page, 'mid': mid})

    # 用户数据
    def parse_user(self, response):
        data = json.loads(response.text)
        if data['ok'] == 1:

            item = WeiboFansSpiderItem()
            item['id'] = data.get('data').get('userInfo').get('id')
            item['statuses_count'] = data.get('data').get('userInfo').get('statuses_count')
            item['screen_name'] = data.get('data').get('userInfo').get('iscreen_named')
            item['profile_url'] = data.get('data').get('userInfo').get('profile_url')
            item['description'] = data.get('data').get('userInfo').get('description')
            item['gender'] = data.get('data').get('userInfo').get('gender')
            item['followers_count'] = data.get('data').get('userInfo').get('followers_count')
            item['follow_count'] = data.get('data').get('userInfo').get('follow_count')

            yield item