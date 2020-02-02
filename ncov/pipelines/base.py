# -*- coding: utf-8 -*-
import logging

from scrapy.exceptions import DropItem
from twisted.internet.threads import deferToThread

from ncov.databases.connections import *

logger = logging.getLogger(__name__)


class BasePipeline(object):

    def process_item(self, item, spider):
        self._check_data(item, spider)
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        return item

    def _check_data(self, item, spider):
        require_fields = getattr(item, 'require_fields', None)
        if require_fields:
            for field in item.require_fields:
                value = item.get(field, None)
                if not value and value != 0:
                    spider.logger.error('Item 数据不完整: %s' % dict(item))
                    raise DropItem()


class MySqlPipeline(BasePipeline):

    def __init__(self):
        self.sql = sql

    def process_item(self, item, spider):
        self._check_data(item, spider)
        return self._process_item(item, spider)

    def _process_item(self, item, spider):
        d = self.sql.runInteraction(self._do_insert, item)
        d.addErrback(self._handle_duplicate_error, item)
        d.addBoth(lambda _: item)
        return d

    def _do_batch_insert(self, txn, items):
        for each in items:
            self._do_insert(txn, each)

    def _do_insert(self, txn, item):
        table = item.table
        unique_fields = getattr(item, 'unique_fields', None)

        exist = None
        if unique_fields:
            where = ' AND '.join(["%s='%s'" % (field, item[field]) for field in unique_fields])
            select_sql = 'SELECT id FROM %s WHERE %s' % (table, where)
            txn.execute(select_sql)
            exist = txn.fetchone()

        if not exist:
            keys = ', '.join(item.keys())
            values = ', '.join(['%s'] * len(item.keys()))
            sql = 'INSERT IGNORE INTO %s (%s) VALUES (%s)' % (table, keys, values)
            txn.execute(sql, tuple(item.values()))

    def _handle_duplicate_error(self, failure, item):
        if failure.value and 'Duplicate' in failure.value.args[1]:
            return
        logger.error('%s\nerror item: %s', failure, item)

    def close_spider(self, spider):
        self.sql.close()
