# -*- coding: utf-8 -*-
import scrapy
import logging
import json
import re
from scrapy.spiders import XMLFeedSpider
from scrapy.exceptions import CloseSpider
from crawling.article_archives import ArticleArchives
from crawling.utils.rule_loader import RuleLoader

class RSSCrawlSpider(XMLFeedSpider):
    name = 'rss_crawl'
    except_regexps = []
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
        self.start_urls  = rules['rss_urls']  # 必須
        self.itertag     = rules['tag_name']  # 必須
        self.link_node   = rules['link_node_name'] # 必須
        for p in params.get('except_article_patterns', []): # 任意
            self.except_regexps.append(re.compile(p))
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
    
    def start_requests(self):
        if self.login_url:
            yield scrapy.Request(
                url=self.login_url,
                callback=self.login,
                dont_filter=True)
        else:
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True)
    
    # TODO: RSSのformログインは動作未確認
    def login(self, response):
        return scrapy.FormRequest.from_response(
                response,
                formdata={self.login_name_attr: self.login_name, self.login_pass_attr: self.login_password},
                callback=self.after_login
            )

    def after_login(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)
    
    # 繰り返しのタグ見つけたら、linkノードからurlを取得する
    def parse_node(self, response, node):
        url = node.xpath(f'./{self.link_node}/text()').extract()[0]
        joined_url = response.urljoin(url)

        # 除外記事
        for r in self.except_regexps:
            if r.search(joined_url):
                logging.debug(f'excepted page [{joined_url}]')
                return
        return scrapy.Request(url=joined_url, callback=self.parse_item)
        
    def parse_item(self, response):
        self.itemcounts += 1
        if self.is_dryrun and self.itemcounts > self.settings['TRIAL_ITEM_COUNT']:
            raise CloseSpider('dryrun stopped')
        item = ArticleArchives()
        item.set(item, response)
        yield item
    