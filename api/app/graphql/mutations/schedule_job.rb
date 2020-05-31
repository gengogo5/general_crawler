require 'httpclient'
module Mutations
  class ScheduleJob < BaseMutation
    graphql_name 'ScheduleJob'
    field :crawl_request, Types::CrawlRequestType, null: true
    field :result, Boolean, null: true

    argument :request_id, ID, required: true
    argument :is_dryrun, Boolean, required: false

    def resolve(**args)
      job = CrawlRequest.find(args[:request_id])

      client = HTTPClient.new
      url = 'http://scrapy:7654/schedule-job.json'

      # dryrunの時は即時実行にする
      is_dryrun = args[:is_dryrun]
      schedule_type = is_dryrun ? 'now' : job.schedule_type

      body = {'project'=> 'crawling',
              'spider' => "#{job.job_type}_crawl",
              'when' => "#{schedule_type}",
              'payload' => "{\"req_id\": #{job.id}, \"is_dryrun\": #{is_dryrun}}"}
      response = client.post(url, body)

      {
        crawl_request: job,
        result: response
      }
    end
  end
end
