# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from scrapy.spiders import XMLFeedSpider
from crawling.article_archives import ArticleArchives

class RSSCrawlSpider(XMLFeedSpider):
    name = 'rss_crawl'

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

    # 繰り返しのタグ見つけたら、linkノードからurlを取得する
    def parse_node(self, response, node):
        url = node.xpath(f'./{self.link_node}/text()').extract()[0]
        logging.info('------------------------------')
        logging.info(url)
        return scrapy.Request(url, self.parse_item)
        
    def parse_item(self, response):
        item = ArticleArchives()
        item.set(item, response)
        yield item
    