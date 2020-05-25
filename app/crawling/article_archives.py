# -*- coding: utf-8 -*-

import scrapy
import gzip
from scrapy.exceptions import DropItem
from datetime import datetime


class ArticleArchives(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()

    def set(self, item, response):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['url'] = response.url # TODO: パラメータ除去

        content_type = response.headers.get('Content-Type').decode('utf-8')
        if 'html' in content_type:
            item['content'] = gzip.compress(bytes(response.text, 'utf-8'))
        else:
            raise DropItem("Missing type in %s" % item)
        item['title'] = response.xpath('//title/text()').extract_first()
        item['updated_at'] = now
        item['created_at'] = now
        return item
