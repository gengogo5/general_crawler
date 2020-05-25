# -*- coding: utf-8 -*-
import textwrap, MySQLdb

class CrawlingPipeline:
    
    def open_spider(self, spider):
        # Spider開始時にDB接続
        settings = spider.settings
        db_info = settings.get('DATABASE')
        self.conn = MySQLdb.connect(**db_info)
    
    def close_spider(self, spider):
        # Spider終了時にDB接続破棄
        self.conn.close()

    def process_item(self, item, spider):
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

