# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class WeiboFansSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = Field()
    statuses_count = Field()
    screen_name = Field()
    profile_url = Field()
    description = Field()
    gender = Field()
    followers_count = Field()
    follow_count = Field()
