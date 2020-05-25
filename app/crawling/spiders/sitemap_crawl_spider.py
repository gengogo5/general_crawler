# -*- coding: utf-8 -*-
import json
import re
import logging
from scrapy.spiders import SitemapSpider
from crawling.article_archives import ArticleArchives

class SitemapCrawlSpider(SitemapSpider):
    name = 'sitemap_crawl'
    sitemap_urls = []
    sitemap_follow = []
    sitemap_rules = []

    # TODO: 重複除外

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 引数から各種設定を取得
        params = json.loads(self.payload)
        sitemap_url = params['sitemap_url'] # 必須
        except_patterns = params['except_article_patterns'] # 任意
        sitemap_patterns = params['sitemap_patterns'] # 任意

        # Seedのサイトマップを追加
        self.sitemap_urls.append(sitemap_url)

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

        # TODO: 圧縮サイトマップをungzipする

    def parse(self, response):
        item = ArticleArchives()
        item.set(item, response)
        yield item
    
    # 除外パターンの場合に使う
    def except_parse(self, response):
        pass
