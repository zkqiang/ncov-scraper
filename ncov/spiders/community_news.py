# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy import Spider, Request

from ..items import NewsItem
from ..utils.area_utils import AreaParser
from ..utils.time_utils import convert_time


class CommunityNewsSpider(Spider):
    name = 'community'

    custom_settings = {
        'ITEM_PIPELINES': {
            'ncov.pipelines.NewsPipeline': 300,
        },
    }

    baidu_url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&medium=0&wd={}'

    primary_kw = ['小区', '社区']

    secondary_kw = ['确诊', '辟谣', '造谣', '封闭', '隔离']

    end_time = datetime(2020, 1, 21, 0, 0, 0, 0)

    area_parser = AreaParser()

    def start_requests(self):
        for kw1 in self.primary_kw:
            for kw2 in self.secondary_kw:
                yield Request(
                    url=self.baidu_url.format(kw1 + '+' + kw2),
                    callback=self.parse_baidu
                )

    def parse_baidu(self, response):
        for res in response.xpath('//div[@id="content_left"]//div[@class="result"]'):
            title = res.xpath('string(./h3/a)').get()
            title = re.sub(r'\s', '', title)
            province, city, district = self.area_parser.parse(title)

            author_node = res.xpath('string(.//p[@class="c-author"])').get()
            author = re.findall(r'(\S+\s?\S+)+', author_node, re.M)

            item = NewsItem(
                title=title,
                link=res.xpath('./h3/a/@href').get(),
                source=author[0],
                publish_time=convert_time(author[1]),
                province=province,
                city=city,
                district=district,
                category=0,
            )

            if item['publish_time'] < self.end_time:
                return None
            yield item

        next_page = response.xpath('.//a[contains(text(), "下一页")]/@href').get()
        if next_page:
            yield Request(
                url=response.urljoin(next_page),
                callback=self.parse_baidu
            )
