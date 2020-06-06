# -*- coding: utf-8 -*-
import scrapy
import json
import re
import logging
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawling.article_archives import ArticleArchives
from crawling.utils.rule_loader import RuleLoader

class RegularCrawlSpider(CrawlSpider):
    name = 'regular_crawl'
    allowed_domains = []
    login_url = None
    itemcounts = 0

    custom_settings = {
      'DUPEFILTER_CLASS': 'crawling.dupefilter.ArticleArchiveDupeFilter',
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 引数から要求IDを取得
        params = json.loads(self.payload)
        self.req_id = params['req_id']
        self.is_dryrun = params.get('is_dryrun', False)

        # DBから各種設定を取得
        rules = RuleLoader.find(self.req_id)
        self.start_urls = rules['start_urls'] # 必須
        index_patterns  = rules.get('index_patterns') # 任意
        allow_patterns  = rules.get('article_patterns') # 必須
        deny_patterns   = rules.get('except_article_patterns', []) # 任意
        shouldFollow    = rules.get('should_follow', False) # 任意
        rp = rules.get('url_replace_pattern','') # 任意
        if rp:
            self.url_replace_pattern = re.compile(rp)
        self.replace_new_string = rules.get('replace_new_string','') # 任意
        if rules.get('user_agent'):
            self.user_agent = rules.get('user_agent')
        ## formログイン関係
        self.login_url = rules.get('login_url')
        self.login_name = rules.get('login_name')
        self.login_password = rules.get('login_password')
        self.login_name_attr = rules.get('login_name_attr')
        self.login_pass_attr = rules.get('login_pass_attr')

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
    
    def start_requests(self):
        if self.login_url:
            yield scrapy.Request(
                url=self.login_url,
                callback=self.login,
                dont_filter=True)
        else:
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True)
    
    def login(self, response):
        return scrapy.FormRequest.from_response(
                response,
                formdata={self.login_name_attr: self.login_name, self.login_pass_attr: self.login_password},
                callback=self.after_login
            )

    def after_login(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)
