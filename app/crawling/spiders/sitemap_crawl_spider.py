# -*- coding: utf-8 -*-
import json
import re
import logging
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.spiders import SitemapSpider
from crawling.article_archives import ArticleArchives
from crawling.utils.rule_loader import RuleLoader

class SitemapCrawlSpider(SitemapSpider):
    name = 'sitemap_crawl'
    sitemap_urls = []
    sitemap_follow = []
    sitemap_rules = []
    url_replace_pattern = None
    login_url = None
    itemcounts = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 引数から要求IDを取得
        params = json.loads(self.payload)
        self.req_id = params['req_id']
        self.is_dryrun = params.get('is_dryrun', False)

        # DBから各種設定を取得
        rules = RuleLoader.find(self.req_id)
        sitemap_url = rules['sitemap_url'] # 必須
        except_patterns = rules.get('except_article_patterns',[]) # 任意
        sitemap_patterns = rules.get('sitemap_patterns',[]) # 任意
        rp = rules.get('url_replace_pattern','') # 任意
        if rp:
            self.url_replace_pattern = re.compile(rp)
        self.replace_new_string = rules.get('replace_new_string','') # 任意

        # Seedのサイトマップを追加
        self.sitemap_urls.append(sitemap_url)

        # ユーザエージェントの書き換え
        if rules.get('user_agent'):
            self.user_agent = rules.get('user_agent')

        # サイトマップindex内の対象パターンを追加
        # 動的にルール追加するためにSitemapSpiderの変数をハック
        for p in sitemap_patterns:
            self._follow.append(re.compile(p))

        # 記事除外ルールを追加
        # 動的にルール追加するためにSitemapSpiderの変数をハック
        for p in except_patterns:
            self._cbs.append((re.compile(p), getattr(self, 'except_parse')))
        # サイトマップ以外はparseする
        self._cbs.append((re.compile('^(?!.*(\.xml|\.xml\.gz)$).*$'), getattr(self, 'parse')))

        ## formログイン関係
        self.login_url = rules.get('login_url')
        self.login_name = rules.get('login_name')
        self.login_password = rules.get('login_password')
        self.login_name_attr = rules.get('login_name_attr')
        self.login_pass_attr = rules.get('login_pass_attr')

        # TODO: 圧縮サイトマップをungzipする
    
    def start_requests(self):
        if self.login_url:
            yield scrapy.Request(
                url=self.login_url,
                callback=self.login,
                dont_filter=True)
        else:
            for url in self.sitemap_urls:
                yield scrapy.Request(url, self._parse_sitemap)

    def login(self, response):
        return scrapy.FormRequest.from_response(
                response,
                formdata={self.login_name_attr: self.login_name, self.login_pass_attr: self.login_password},
                callback=self.after_login
            )

    # ログイン後は通常ルートと同じ
    def after_login(self, response):
        for url in self.sitemap_urls:
            yield scrapy.Request(url, self._parse_sitemap)

    def parse(self, response):
        # dryrun設定
        self.itemcounts += 1
        if self.is_dryrun and self.itemcounts > self.settings['TRIAL_ITEM_COUNT']:
            raise CloseSpider('dryrun stopped')
        item = ArticleArchives()
        item.set(item, response)
        yield item
    
    # 除外パターンの場合に使う
    def except_parse(self, response):
        pass
