require 'httpclient'
module Mutations
  class ScheduleJob < BaseMutation
    graphql_name 'ScheduleJob'
    field :crawl_request, Types::CrawlRequestType, null: true
    field :is_dryrun, Boolean, null: true
    field :result, String, null: true

    argument :request_id, ID, required: true
    argument :is_dryrun, Boolean, required: false

    def resolve(**args)
      job = CrawlRequest.find(args[:request_id])

      client = HTTPClient.new
      url = 'http://scrapy:7654/schedule-job.json'

      # dryrunの時は即時実行にする
      is_dryrun = args[:is_dryrun]
      schedule = if is_dryrun || job.schedule_type == 'now'
                   'now'
                 elsif job.schedule_type == 'intervals'
                   "every #{job.interval_hours} hours" 
                 else
                   raise GraphQL::ExecutionError.new('schedule type is invalid.')
                 end

      body = {'project'=> 'crawling',
              'spider' => "#{job.job_type}_crawl",
              'when' => "#{schedule}",
              'payload' => "{\"req_id\": #{job.id}, \"is_dryrun\": #{is_dryrun}}"}
      res = client.post(url, body)

      # 即時実行でない場合は定期実行されるのでジョブIDを登録する
      resj = JSON.parse(res.body)
      if resj['status'] == 'ok' && schedule != 'now'
          job.update(job_id: resj['identifier'])
      end

      {
        crawl_request: job,
        is_dryrun: is_dryrun,
        result: resj['status']
      }
    end
  end
end
