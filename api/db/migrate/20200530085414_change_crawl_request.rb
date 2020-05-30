class ChangeCrawlRequest < ActiveRecord::Migration[5.2]
  def change
    change_column :crawl_requests, :rules, :text
  end
end
