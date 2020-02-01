# -*- coding: utf-8 -*-
import json
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
                    if area['name'].rstrip('市') in text:
                        return province['name'], city['name'], area['name']
                if city['name'].rstrip('市') in text:
                    return province['name'], city['name'], None
            if province['shortName'] in text:
                return province['name'], None, None
        return None, None, None

    def parse_province(self, text: str) -> str or None:
        for province in self._area_data:
            if province['shortName'] in text:
                return province['name']
        return None
