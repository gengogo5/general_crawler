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

  desc "scrapyのログを表示する"
  task :log do
    sh "docker-compose logs scrapy"
  end
end

namespace :mysql do
  desc "mysqlのマイグレーション"
  task :migrate do
    sh "docker-compose exec api rake db:migrate"
  end
end

namespace :rails do
  desc "railsコンソールを開く"
  task :console do
    sh "docker-compose exec api bundle exec rails c"
  end
end

namespace :scrapy do
  namespace :job do
    desc "scrapydのジョブを停止する"
    task :stop, ['id'] do |task, args|
      sh "docker-compose exec scrapy scrapy-do-cl cancel-job --job-id #{args.id}"
    end

    desc "scrapydジョブのログを表示する"
    task :log, ['id'] do |task, args|
      sh "docker-compose exec scrapy scrapy-do-cl get-log --job-id #{args.id}" 
    end
  end
end