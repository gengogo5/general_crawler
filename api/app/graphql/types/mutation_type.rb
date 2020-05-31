module Types
  class MutationType < Types::BaseObject
    field :create_regular_crawl_request, mutation: Mutations::CreateRegularCrawlRequest
    field :create_sitemap_crawl_request, mutation: Mutations::CreateSitemapCrawlRequest
    field :create_rss_crawl_request, mutation: Mutations::CreateRssCrawlRequest
    # TODO: 更新と削除
    field :delete_crawl_request, mutation: Mutations::DeleteCrawlRequest
    field :update_crawl_request, mutation: Mutations::UpdateCrawlRequest
    field :schedule_job, mutation: Mutations::ScheduleJob
    field :cancel_job, mutation: Mutations::CancelJob
    # TODO: remove me
    field :test_field, String, null: false,
      description: "An example field added by the generator"
    def test_field
      "Hello World"
    end
  end
end
