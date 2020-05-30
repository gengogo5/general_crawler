require 'json'
module Mutations
  class CreateCrawlRequest < BaseMutation
    graphql_name 'CreateCrawlRequest'
    field :crawl_request, Types::CrawlRequestType, null: true
    field :result, Boolean, null: true

    argument :job_type, String, required: true
    argument :rss_urls, [String], required: false
    argument :tag_name, String, required: false
    argument :link_node_name, String, required: false
    argument :schedule_type, String, required: false

    def resolve(**args)
      request = CrawlRequest.create(
        job_type: args[:job_type],
        rules: JSON.generate(
          { :rss_urls => args[:rss_urls],
            :tag_name => args[:tag_name],
            :link_node_name => args[:link_node_name]
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
