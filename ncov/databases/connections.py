# -*- coding: utf-8 -*-
from warnings import filterwarnings

import pymysql
from twisted.enterprise import adbapi

from ncov import settings

filterwarnings("error", category=pymysql.Warning)

_sql_params = dict(
    host=settings.MYSQL_HOST,
    db=settings.MYSQL_DB,
    user=settings.MYSQL_USER,
    passwd=settings.MYSQL_PASSWORD,
    port=settings.MYSQL_PORT,
    charset=settings.MYSQL_CHARSET,
    cursorclass=pymysql.cursors.DictCursor,
    use_unicode=True,
    cp_reconnect=True,
    cp_max=10,
    autocommit=True,
)

sql = adbapi.ConnectionPool('pymysql', **_sql_params)
