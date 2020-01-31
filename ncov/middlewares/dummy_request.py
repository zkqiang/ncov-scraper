# -*- coding: utf-8 -*-
from scrapy.http import HtmlResponse


class DummyRequestMiddleware(object):

    def process_request(self, request, spider):
        if request.url == ':':
            return HtmlResponse(url=request.url)
