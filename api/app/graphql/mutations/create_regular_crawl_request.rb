module Mutations
  class CreateRegularCrawlRequest < BaseMutation
    graphql_name 'CreateRegularCrawlRequest'
    field :crawl_request, Types::CrawlRequestType, null: true
    field :result, Boolean, null: true

    argument :job_type, String, required: true
    argument :start_urls, [String], required: true
    argument :index_patterns, [String], required: false
    argument :article_patterns, [String], required: false
    argument :except_article_patterns, [String], required: false
    argument :should_follow, Int, required: false
    argument :url_replace_pattern, String, required: false
    argument :replace_new_string, String, required: false
    argument :user_agent, String, required: false
    argument :schedule_type, String, required: false
    argument :interval_hours, Int, required: false

    def resolve(**args)
      request = CrawlRequest.create(
        job_type: args[:job_type],
        rules: JSON.generate(
          { start_urls: args[:start_urls],
            index_patterns: args[:index_patterns],
            article_patterns: args[:article_patterns],
            except_article_patterns: args[:except_article_patterns],
            should_follow: args[:should_follow],
            url_replace_pattern: args[:url_replace_pattern],
            replace_new_string: args[:replace_new_string],
            user_agent: args[:user_agent],
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
