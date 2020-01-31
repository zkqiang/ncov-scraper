# -*- coding: utf-8 -*-
import random


class RandomUserAgentMiddleware(object):
    """
    注意使用时需要将原生 useragent.UserAgentMiddleware 设置为 None
    """

    def __init__(self, user_agents):
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        h = cls(crawler.settings['USER_AGENTS'])
        return h

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        request.headers['User-Agent'] = user_agent
