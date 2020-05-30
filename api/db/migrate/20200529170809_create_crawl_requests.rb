class CreateCrawlRequests < ActiveRecord::Migration[5.2]
  def change
    create_table :crawl_requests do |t|
      t.string :job_id
      t.string :job_type, null: false
      t.json   :rules
      t.string :schedule_type, null: false
      t.integer    :interval_hours
      t.timestamps
    end
  end
end
