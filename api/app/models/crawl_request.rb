class CrawlRequest < ApplicationRecord

  after_find :parse_rules
  attr_accessor :rss_urls,
                :tag_name,
                :link_node_name,
                :except_article_patterns,
                :start_urls,
                :index_patterns,
                :article_patterns,
                :sitemap_url,
                :sitemap_patterns

  private

  # JSONのクロール設定をparseする
  def parse_rules
    self.rss_urls = {:rss_urls => self[:rules]['rss_urls']}
    self.tag_name = {:tag_name => self[:rules]['tag_name']}
    self.link_node_name = {:link_node_name => self[:rules]['link_node_name']}
    self.except_article_patterns = {:except_article_patterns => self[:rules]['except_article_patterns']}
    self.start_urls = {:start_urls => self[:rules]['start_urls']}
    self.index_patterns = {:index_patterns => self[:rules]['index_patterns']}
    self.article_patterns = {:article_patterns => self[:rules]['article_patterns']}
    self.sitemap_url = {:sitemap_url => self[:rules]['sitemap_url']}
    self.sitemap_patterns = {:sitemap_patterns => self[:rules]['sitemap_patterns']}
  end
end
