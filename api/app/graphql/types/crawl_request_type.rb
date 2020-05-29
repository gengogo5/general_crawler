module Types
  class CrawlRequestType < Types::BaseObject
    field :id, ID, null: false
    field :job_id, String, null: true
    field :job_type, String, null: false
    field :rules, String, null: true
    field :schedule_type, String, null: true
    field :interval_hours, Integer, null: true
  end
end
