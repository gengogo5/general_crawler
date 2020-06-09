class CrawlRequest < ApplicationRecord

  after_find :parse_rules
  attr_accessor :start_urls,
                :index_patterns,
                :article_patterns,
                :except_article_patterns,
                :should_follow,
                :url_replace_pattern,
                :replace_new_string,
                :user_agent,
                :login_url,
                :login_name,
                :login_password,
                :login_name_attr,
                :login_pass_attr,
                :tag_name,
                :link_node_name,
                :sitemap_patterns,
                :url_prefix

  private

  # JSONのクロール設定をparseする
  # TODO: パラメータが確定したらクエリ用に全部書く
  def parse_rules
    rulesj = JSON.parse(self[:rules])
    self.start_urls              = rulesj['start_urls']
    self.index_patterns          = rulesj['index_patterns']
    self.article_patterns        = rulesj['article_patterns']
    self.except_article_patterns = rulesj['except_article_patterns']
    self.should_follow           = rulesj['should_follow']
    self.url_replace_pattern     = rulesj['url_replace_pattern']
    self.replace_new_string      = rulesj['replace_new_string']
    self.user_agent              = rulesj['user_agent']
    self.login_url               = rulesj['login_url']
    self.login_name              = rulesj['login_name']
    self.login_password          = rulesj['login_password']
    self.login_name_attr         = rulesj['login_name_attr']
    self.login_pass_attr         = rulesj['login_pass_attr']
    self.tag_name                = rulesj['tag_name']
    self.link_node_name          = rulesj['link_node_name']
    self.sitemap_patterns        = rulesj['sitemap_patterns']
    self.url_prefix              = rulesj['url_prefix']
  end
end
