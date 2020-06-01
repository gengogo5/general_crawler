# -*- coding: utf-8 -*-
import textwrap, MySQLdb
import logging
import re
import boto3

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
        # URL置換対応
        # subの第2引数に正規表現オブジェクトが使えないので後方参照は不可
        # dryrun用pipelineに渡す為にスキップより前に実行
        if spider.url_replace_pattern:
            item['url'] = re.sub(spider.url_replace_pattern, \
                                 spider.replace_new_string, \
                                 item['url'])
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
        self.url_list = []

    def close_spider(self, spider):
        if not spider.is_dryrun: return
        # S3に書き込む
        # 環境変数からurlが取れなかったのでとりあえずベタ書きする
        s3 = boto3.resource('s3', endpoint_url='http://minio:9000', \
                                  aws_access_key_id='accessKey', \
                                  aws_secret_access_key='secretKey', \
                                  region_name='us-east-1')
        bucket_name = 'crawl-data'
        bucket = s3.Bucket(bucket_name)
        bucket.put_object(Key=f'{spider.req_id}/urllist.txt', Body = '\n'.join(self.url_list))

    def process_item(self, item, spider):
        if not spider.is_dryrun: return item
        self.url_list.append(item['url'])
        return item
