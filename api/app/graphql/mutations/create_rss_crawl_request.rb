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
    argument :schedule_type, String, required: false

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
          }
        ),
        schedule_type: args[:schedule_type]       
      )
      {
        crawl_request: request,
        result: request.errors.blank?
      }
    end
  end
end
