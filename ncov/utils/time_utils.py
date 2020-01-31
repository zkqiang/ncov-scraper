# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta


def convert_time(t: str) -> datetime:
    offset = int(re.findall(r'\d+', t)[0])

    if '秒前' in t:
        s = (datetime.now() - timedelta(seconds=offset))

    elif '分钟前' in t:
        s = (datetime.now() - timedelta(minutes=offset))

    elif '小时前' in t:
        s = (datetime.now() - timedelta(hours=offset))

    elif '天前' in t:
        s = (datetime.now() - timedelta(days=offset))

    else:
        s = datetime.strptime(t, "%Y年%m月%d日 %H:%M")

    return s
