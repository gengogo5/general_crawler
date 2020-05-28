namespace :server do
  desc "サーバを起動する"
  task :start do
    sh "docker-compose up"
  end

  desc "サーバを停止する"
  task :stop do
    sh "docker-compose down"
    sh "rm app/projects/schedule.db.bak*"
  end
end

namespace :scrapy do
  desc "scrapyプロジェクトをpushする"
  task :push do
    sh "docker-compose exec scrapy scrapy-do-cl push-project"
  end

  desc "scrapyのジョブリストを表示する"
  task :joblist do
    sh "docker-compose exec scrapy scrapy-do-cl list-jobs"
  end
end

