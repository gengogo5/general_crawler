# -*- coding: utf-8 -*-
from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.project import get_project_settings
import re
import textwrap, MySQLdb

class ArticleArchiveDupeFilter(RFPDupeFilter):

    # inject from CustomScheduler
    spider = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        params = settings.get('DATABASE')
        self.conn = MySQLdb.connect(**params)
        self.conn.autocommit(True)

    def request_seen(self, request):
        # 既存の重複判定
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + '\n')

        # 独自の重複判定(登録済みレコード判定)
        request_url = request.url
        if 'url_replace_pattern' in dir(self.spider):
            request_url = re.sub(self.spider.url_replace_pattern, \
                                 self.spider.replace_new_string, \
                                 request_url)

        sql = textwrap.dedent('''\
        SELECT id
          FROM article_archives
         WHERE url = %(url)s
        ''')
        c = self.conn.cursor()
        c.execute(sql, {'url': request_url})
        return c.rowcount > 0

    # 後処理をオーバライド
    def close(self, reason):
        self.conn.close()
