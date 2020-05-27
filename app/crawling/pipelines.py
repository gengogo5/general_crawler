# -*- coding: utf-8 -*-
import textwrap, MySQLdb
import logging

class CrawlingPipeline:
    
    def open_spider(self, spider):
        if spider.is_dryrun: return
        # Spider開始時にDB接続
        settings = spider.settings
        db_info = settings.get('DATABASE')
        self.conn = MySQLdb.connect(**db_info)
    
    def close_spider(self, spider):
        if spider.is_dryrun: return
        # Spider終了時にDB接続破棄
        self.conn.close()

    def process_item(self, item, spider):
        if spider.is_dryrun: return item

        sql = textwrap.dedent('''\
        REPLACE INTO article_archives (
            url,
            content,
            title,
            updated_at,
            created_at
        ) VALUES (
            %(url)s,
            %(content)s,
            %(title)s,
            %(updated_at)s,
            %(created_at)s
        )
        ''')
        try:
            c = self.conn.cursor()
            c.execute(sql, dict(item))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        return item

# spiderの変数でdryrun有無を判定する
# もう少しいい方法があるかもしれない
class DryRunPipeline:

    def open_spider(self, spider):
        if not spider.is_dryrun: return
        self.file = open('tmp/items.txt', 'w')

    def close_spider(self, spider):
        if not spider.is_dryrun: return
        self.file.close()

    def process_item(self, item, spider):
        if not spider.is_dryrun: return item
        line = item['url'] + "\n"
        self.file.write(line)
        return item
