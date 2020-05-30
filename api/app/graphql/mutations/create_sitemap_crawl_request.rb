module Mutations
  class CreateSitemapCrawlRequest < BaseMutation
    graphql_name 'CreateSitemapCrawlRequest'
    field :crawl_request, Types::CrawlRequestType, null: true
    field :result, Boolean, null: true

    argument :job_type, String, required: true
    argument :sitemap_url, String, required: true
    argument :sitemap_patterns, [String], required: false
    argument :except_article_patterns, [String], required: false
    argument :schedule_type, String, required: false
    argument :interval_hours, Int, required: false

    def resolve(**args)
      request = CrawlRequest.create(
        job_type: args[:job_type],
        rules: JSON.generate(
          { :sitemap_url => args[:sitemap_url],
            :sitemap_patterns => args[:sitemap_patterns],
            :except_article_patterns => args[:except_article_patterns]
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
