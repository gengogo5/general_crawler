module Types
  class CrawlRequestType < Types::BaseObject
    field :id, ID, null: false
    field :job_id, String, null: true
    field :job_type, String, null: false
    field :rules, String, null: true
    field :start_urls, [String], null: true
    field :index_patterns, [String], null: true
    field :article_patterns, [String], null: true
    field :except_article_patterns, [String], null: true
    field :should_follow, Integer, null: true
    field :url_replace_pattern, String, null: true
    field :replace_new_string, String, null: true
    field :user_agent, String, null: true
    field :login_url,  String, null: true
    field :login_name, String, null: true
    field :login_password, String, null: true
    field :login_name_attr, String, null: true
    field :login_pass_attr, String, null: true
    field :tag_name,        String, null: true
    field :link_node_name,  String, null: true
    field :sitemap_patterns, [String], null: true
    field :url_prefix, String, null: true
    field :is_dryrun, Boolean, null: true
    field :schedule_type, String, null: true
    field :interval_hours, Integer, null: true
  end
end
