# -*- coding: utf-8 -*-
import json
import re
from os import path


class AreaParser(object):

    def __init__(self):
        file = path.join(path.dirname(__file__), 'area.json')
        with open(file, 'r') as f:
            self._area_data = json.load(f)

    def parse(self, text: str) -> (str or None, str or None, str or None):
        for province in self._area_data:
            for city in province['cityList']:
                for area in city['areaList']:
                    if self._abbrev(area['name']) in text:
                        return province['name'], city['name'], area['name']
                if self._abbrev(city['name']) in text:
                    return province['name'], city['name'], None
            if self._abbrev(province['name']) in text:
                return province['name'], None, None
        return None, None, None

    @staticmethod
    def _abbrev(name: str) -> str:
        return re.sub(r'[省市]', '', name)
