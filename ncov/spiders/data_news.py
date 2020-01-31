# -*- coding: utf-8 -*-
import json
from datetime import datetime

from scrapy import Spider, Request

from ..items import NewsItem


class DataNewsSpider(Spider):
    name = 'data'

    custom_settings = {
        'ITEM_PIPELINES': {
            'ncov.pipelines.NewsPipeline': 300,
        },
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'file1.dxycdn.com',
            'Referer': 'https://ncov.dxy.cn/ncovh5/view/pneumonia_timeline?whichFrom=dxy'
        },
    }

    dxy_url = 'https://file1.dxycdn.com/2020/0130/492/3393874921745912795-115.json'

    limit = None

    def __init__(self, limit=100, *a, **kw):
        super().__init__(*a, **kw)
        self.limit = int(limit) if limit else None

    def start_requests(self):
        yield Request(
            url=self.dxy_url,
            callback=self.parse_dxy
        )

    def parse_dxy(self, response):
        data = json.loads(response.text)
        for d in data['data'][:self.limit]:
            yield NewsItem(
                title=d['title'],
                link=d['sourceUrl'],
                source=d.get('infoSource', None),
                publish_time=datetime.fromtimestamp(int(d['pubDate']) / 1000),
                province=d.get('provinceName', None),
                category=1,
            )
