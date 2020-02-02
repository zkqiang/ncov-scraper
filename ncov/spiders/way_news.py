# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy import Spider, Request

from ..items import NewsItem
from ..utils.area_utils import AreaParser


class WayNewsSpider(Spider):
    name = 'way'

    custom_settings = {
        'ITEM_PIPELINES': {
            'ncov.pipelines.NewsPipeline': 300,
        },
    }

    start_urls = ['http://www.0512s.com/lukuang/']

    area_parser = AreaParser()

    def parse(self, response):
        for href in response.xpath('//div[@id="introContent"]/div[1]/p/a'):
            yield Request(
                url=response.urljoin(href.xpath('./@href').get()),
                meta={'province': href.xpath('./text()').get()},
                callback=self.parse_news
            )

    def parse_news(self, response):
        for text in response.xpath('//div[@class="lc"]/text()').getall():
            date_title = re.findall(r'(^\d{4}-\d{2}-\d{2} \d{2}:\d{2}) (.+)', text)
            if not date_title or len(date_title[0]) < 2:
                continue

            date = datetime.strptime(date_title[0][0], '%Y-%m-%d %H:%M')
            title = re.sub(r'^[\t\s]+|[\t\s]+$', '', date_title[0][1])
            title = re.sub(r'^【.+?】|[\t\n]', '', title, re.M)

            if len(title) > 150:
                continue

            item = NewsItem(
                title=title,
                publish_time=date,
                province=self.area_parser.parse_province(response.meta['province']),
                category=2,
            )
            item.__class__.require_fields = ['title', 'publish_time', 'category', 'province']
            item.__class__.unique_fields = ['province', 'publish_time']
            yield item
