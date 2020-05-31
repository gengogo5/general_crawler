module Mutations
  class CancelJob < BaseMutation
    graphql_name 'CancelJob'
    field :crawl_request, Types::CrawlRequestType, null: true
    field :result, Boolean, null: true

    argument :request_id, ID, required: true

    def resolve(**args)
      job = CrawlRequest.find(args[:request_id])

      client = HTTPClient.new
      url = 'http://scrapy:7654/cancel-job.json'

      response = client.post(url, {id: job.job_id})

      resj = JSON.parse(response.body)
      if resj['status'] == 'ok'
          job.update(job_id: nil)
      end
      {
        crawl_request: job,
        result: response.status
      }
    end
  end
end
