# general_crawler
汎用クローラのプロトタイプ

## 補助コマンド
Rakeで補助コマンドを提供する

### コンテナ操作

```bash
# コンテナ起動
rake server:start

# コンテナ停止
rake server:stop

```

### scrapy操作

```bash
# プロジェクトをpush(再push含む)
rake scrapy:push

# 起動中のジョブリストを表示
rake scrapy:joblist

# scrapydのログを表示
rake scrapy:log

```

### rails操作

```bash

# railsコンテナでマイグレーション
rake mysql:migrate

# railsコンソール
rake rails:console

```

### scrapyジョブ操作

```bash

# ジョブの停止
rake scrapy:job:stop[#{job_id}]

# ジョブのログを表示
rake scrapy:job:log[#{job_id}]

```
