require 'json'
module Mutations
  class CreateRevisitCrawlRequest < BaseMutation
    graphql_name 'CreateRevisitCrawlRequest'
    field :crawl_request, Types::CrawlRequestType, null: true
    field :result, Boolean, null: true

    argument :job_type, String, required: true
    argument :url_prefix, String, required: true
    argument :schedule_type, String, required: false
    argument :interval_hours, Int, required: false

    def resolve(**args)
      request = CrawlRequest.create(
        job_type: args[:job_type],
        rules: JSON.generate(
          { 
            url_prefix: args[:url_prefix],
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
