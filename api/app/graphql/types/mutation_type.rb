module Types
  class MutationType < Types::BaseObject
    field :create_regular_crawl_request, mutation: Mutations::CreateRegularCrawlRequest
    field :create_sitemap_crawl_request, mutation: Mutations::CreateSitemapCrawlRequest
    field :create_rss_crawl_request, mutation: Mutations::CreateRssCrawlRequest
    field :create_revisit_crawl_request, mutation: Mutations::CreateRevisitCrawlRequest
    field :delete_crawl_request, mutation: Mutations::DeleteCrawlRequest
    field :schedule_job, mutation: Mutations::ScheduleJob
    field :cancel_job, mutation: Mutations::CancelJob
    # TODO: 更新
    field :update_crawl_request, mutation: Mutations::UpdateCrawlRequest
  end
end
