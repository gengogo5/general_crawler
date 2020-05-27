# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawling.article_archives import ArticleArchives

class RegularCrawlSpider(CrawlSpider):
    name = 'regular_crawl'
    allowed_domains = []
    itemcounts = 0

    custom_settings = {
        'DUPEFILTER_CLASS': 'crawling.dupefilter.ArticleArchiveDupeFilter'
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 引数から各種設定を取得
        params = json.loads(self.payload)
        self.start_urls = params['start_urls'] # 必須
        index_patterns  = params.get('index_patterns') # 任意
        allow_patterns  = params.get('article_patterns') # 必須
        deny_patterns   = params.get('except_article_patterns', []) # 任意
        shouldFollow    = params.get('should_follow', False) # 任意
        self.is_dryrun  = params.get('is_dryrun', False) # 任意

        # ルール設定
        # TODO: 正規表現を事前サニタイズするかどうか(検証済を受け入れる前提でも可)
        raw_rule = []
        if index_patterns:
            raw_rule.append(Rule(LinkExtractor(allow=tuple(index_patterns))))
        raw_rule.append(Rule(LinkExtractor(allow=tuple(allow_patterns), \
                                           deny=tuple(deny_patterns)), \
                                           follow=shouldFollow, \
                                           callback='parse_item'))

        self.rules = tuple(raw_rule)
        self._compile_rules() # 動的なルール生成に必要

    def parse_item(self, response):
        # dryrun設定
        self.itemcounts += 1
        if self.is_dryrun and self.itemcounts > self.settings['TRIAL_ITEM_COUNT']:
            raise CloseSpider('dryrun stopped')

        item = ArticleArchives()
        item.set(item, response)
        yield item
    