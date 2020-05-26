# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re
from scrapy.spiders import XMLFeedSpider
from crawling.article_archives import ArticleArchives

class RSSCrawlSpider(XMLFeedSpider):
    name = 'rss_crawl'
    except_regexps = []

    custom_settings = {
        'DUPEFILTER_CLASS': 'crawling.dupefilter.ArticleArchiveDupeFilter'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 引数から各種設定を取得
        params = json.loads(self.payload)
        self.start_urls  = params['rss_urls']  # 必須
        self.itertag     = params['tag_name']  # 必須
        self.link_node   = params['link_node_name'] # 必須
        self.is_dryrun   = params.get('is_dryrun', False) # 任意
        for p in params.get('except_article_patterns', []): # 任意
            self.except_regexps.append(re.compile(p))

    # 繰り返しのタグ見つけたら、linkノードからurlを取得する
    def parse_node(self, response, node):
        url = node.xpath(f'./{self.link_node}/text()').extract()[0]
        joined_url = response.urljoin(url)

        # 除外記事
        for r in self.except_regexps:
            if r.search(joined_url):
                logging.debug(f'excepted page [{joined_url}]')
                return
        return scrapy.Request(joined_url, self.parse_item)
        
    def parse_item(self, response):
        item = ArticleArchives()
        item.set(item, response)
        yield item
    