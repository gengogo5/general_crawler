module Mutations
  class DeleteCrawlRequest < BaseMutation
    graphql_name 'DeleteCrawlRequest'
    field :crawl_request, Types::CrawlRequestType, null: true
    field :result, Boolean, null: true

    argument :request_id, ID, required: true

    def resolve(**args)
      job = CrawlRequest.find(args[:request_id])

      # スケジュール済みの場合は停止してから削除
      # 若干やりすぎ感はある。スケジュール済みはエラーで返しても良いかもしれない
      if job.job_id.present?
        client = HTTPClient.new
        url = 'http://scrapy:7654/cancel-job.json'
        client.post(url, {id: job.job_id})
      end
      {
        result: job.destroy
      }
    end
  end
end
