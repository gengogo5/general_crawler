# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawling.article_archives import ArticleArchives

class RegularCrawlSpider(CrawlSpider):
    name = 'regular_crawl'
    allowed_domains = []

    custom_settings = {
        'DUPEFILTER_CLASS': 'crawling.dupefilter.ArticleArchiveDupeFilter'
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 引数から各種設定を取得
        params = json.loads(self.payload)
        self.start_urls = params['start_urls'] # 必須
        index_patterns  = params['index_patterns'] # 任意
        allow_patterns  = params['article_patterns'] # 任意
        deny_patterns   = params['except_article_patterns'] # 任意

        # ルール設定
        # TODO: raw_ruleは最初からrules変数使っていいかもしれない(項目数が可変か検討)
        # TODO: 正規表現を事前サニタイズするかどうか(検証済を受け入れる前提でも可)
        # TODO: followの制御フラグ
        raw_rule = []
        raw_rule.append(Rule(LinkExtractor(allow=tuple(index_patterns))))
        raw_rule.append(Rule(LinkExtractor(allow=tuple(allow_patterns), deny=tuple(deny_patterns)), follow=False, callback='parse_item'))

        self.rules = tuple(raw_rule)
        self._compile_rules() # 動的なルール生成に必要

    def parse_item(self, response):
        item = ArticleArchives()
        item.set(item, response)
        yield item
    