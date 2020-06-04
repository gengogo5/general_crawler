require 'json'
module Mutations
  class CreateRssCrawlRequest < BaseMutation
    graphql_name 'CreateRssCrawlRequest'
    field :crawl_request, Types::CrawlRequestType, null: true
    field :result, Boolean, null: true

    argument :job_type, String, required: true
    argument :rss_urls, [String], required: false
    argument :tag_name, String, required: false
    argument :link_node_name, String, required: false
    argument :url_replace_pattern, String, required: false
    argument :replace_new_string, String, required: false
    argument :user_agent, String, required: false
    argument :login_url, String, required: false
    argument :login_name, String, required: false
    argument :login_password, String, required: false
    argument :login_name_attr, String, required: false
    argument :login_pass_attr, String, required: false
    argument :schedule_type, String, required: false
    argument :interval_hours, Int, required: false

    def resolve(**args)
      request = CrawlRequest.create(
        job_type: args[:job_type],
        rules: JSON.generate(
          { rss_urls: args[:rss_urls],
            tag_name: args[:tag_name],
            link_node_name: args[:link_node_name],
            url_replace_pattern: args[:url_replace_pattern],
            replace_new_string: args[:replace_new_string],
            user_agent: args[:user_agent],
            login_url: args[:login_url],
            login_name: args[:login_name],
            login_password: args[:login_password],
            login_name_attr: args[:login_name_attr],
            login_pass_attr: args[:login_pass_attr],
          }
        ),
        schedule_type: args[:schedule_type],    
        interval_hours: args[:interval_hours]   
      )
      {
        crawl_request: request,
        result: request.errors.blank?
      }
    end
  end
end
