# -*- coding: utf-8 -*-
from scrapy import Item, Field


class NewsItem(Item):
    table = 'tb_news'
    require_fields = ['title', 'link', 'publish_time', 'category']
    unique_fields = ['link']

    title = Field()
    link = Field()
    source = Field()
    publish_time = Field()
    province = Field()
    city = Field()
    district = Field()
    place = Field()
    category = Field()
