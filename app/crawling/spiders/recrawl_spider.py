# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings
from crawling.article_archives import ArticleArchives
from crawling.utils.rule_loader import RuleLoader
import json
import textwrap, MySQLdb

class RecrawlSpider(Spider):
    name = 'revisit_crawl'
    start_urls = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        params = json.loads(self.payload)
        self.req_id = params['req_id']

        # DBから各種情報を取得
        rules = RuleLoader.find(self.req_id)
        url_prefix = rules['url_prefix']
        self.is_dryrun = params.get('is_dryrun', False)

        if len(url_prefix) > 0:
            url = url_prefix + '%'
        settings = get_project_settings()
        db_info = settings.get('DATABASE')
        conn = MySQLdb.connect(**db_info)
        # TODO: urlにインデックス貼らないと遅い
        sql = textwrap.dedent('''\
        SELECT url
          FROM article_archives
         WHERE url LIKE %(url)s;
        ''')
        c = conn.cursor()
        c.execute(sql, {'url': url})
        for r in c:
            self.start_urls.append(r[0])
        conn.close()

    def parse(self, response):
        item = ArticleArchives()
        item.set(item, response)
        yield item
