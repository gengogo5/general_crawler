# -*- coding: utf-8 -*-
from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.project import get_project_settings
import textwrap, MySQLdb

class ArticleArchiveDupeFilter(RFPDupeFilter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        params = settings.get('DATABASE')
        self.conn = MySQLdb.connect(**params)
        self.conn.autocommit(True)

    # DBに重複レコードがあったら既知と判断してDROP
    def request_seen(self, request):
        sql = textwrap.dedent('''\
        SELECT id
          FROM article_archives
         WHERE url = %(url)s
        ''')
        c = self.conn.cursor()
        c.execute(sql, {'url': request.url})
        return c.rowcount > 0

    # 後処理をオーバライド
    def close(self, reason):
        self.conn.close()
