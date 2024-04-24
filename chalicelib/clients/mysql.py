import os
from functools import lru_cache

import pymysql
import pymysqlpool


class Mysql(object):
    def __init__(self):
        self.debug = False
        self.host = os.environ.get("MYSQL_HOST")
        self.user = os.environ.get("MYSQL_USER")
        self.password = os.environ.get("MYSQL_PASSWORD")
        self.db = os.environ.get("MYSQL_DB")
        self.pool = None

    def _create_pool(self):
        self.pool = pymysqlpool.ConnectionPool(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
        )

    def reconnect(self):
        self.pool = None
        self._create_pool()

    def _get_connection(self):
        if not self.pool:
            self._create_pool()
        connection = self.pool.get_connection()
        return connection

    @lru_cache(maxsize=None)
    def execute(self, query):
        connection = self._get_connection()
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute(query)
        result = list(cur)
        cur.close()
        connection.commit()
        connection.close()
        return result


mysql = Mysql()
