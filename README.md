# general_crawler
汎用クローラのプロトタイプ

RSSとかサイトマップとかから、いい感じに記事を取ってくるだけのクローラ。スクレイピングはしない。

## 構成
| 分野 | 実装 |
|:---:|:---:|
|クローラ|Scrapy|
|スケジューラ|scrapy-do|
|DB|MySQL|
|API|Rails(GraphQL)|
|画面|なんでもいい|
|その他|S3(minio)|

ポートとかの詳細は`docker-compose.yml`参照

## 初期設定
### 事前インストール

- [insomnia](https://insomnia.rest/graphql/)
- docker
- ruby

### 手順
1. `docker-compose build`

2. `rake server:start`

3. `rake mysql:migrate`

4. `rake scrapy:push`

5. http://localhost:9001 でminioブラウザにアクセスして`crawl-data`バケットを作成

6. Insomniaからクロール設定登録(次項参照)

## API(GraphQL)

<details>

<summary>クロール設定(サイトマップ)</summary>

```graphql

mutation {
  createSitemapCrawlRequest(
    input: {
      jobType: "sitemap",
      sitemapUrl: "https://example.com/sitemap.xml",
      sitemapPatterns: ["sitemap-pt-post-2020-01"],
      exceptArticlePatterns: ["https://example.com/99999"],
      scheduleType: "now",
    }) {
    crawlRequest {
      id
      rules
    }
    result
  }
}
```

</details>


<details>

<summary>クロール設定(RSS)</summary>

```graphql

mutation {
  createRssCrawlRequest(
    input: {
      jobType: "rss",
      rssUrls: ["https://news.example.com/rss/foobar.xml"],
      tagName: "item",
      linkNodeName: "link",
      scheduleType: "now",
    }) {
    crawlRequest {
      id
      rules
    }
    result
  }
}
```

</details>

<details>

<summary>クロール設定(サイトトップ)</summary>

```graphql

mutation {
  createRegularCrawlRequest(
    input: {
      jobType: "regular",
      startUrls: ["https://corp.example.com/blog/articles"],
      indexPatterns: ["https://corp.example.com/blog/articles/page/[2|3]"],
      articlePatterns: ["https://corp.example.com/blog/\\d+"],
      exceptArticlePatterns:[],
      scheduleType: "intervals",
      intervalHours: 3
    }) {
    crawlRequest {
      id
      rules
    }
    result
  }
}
```

</details>


<details>

<summary>ジョブ登録</summary>

```graphql

mutation {
  scheduleJob(
    input: {
      requestId: 4,
      isDryrun: true
    }) {
    result
    isDryrun
  }
}

```

</details>

<details>

<summary>ジョブ停止</summary>

```graphql

mutation {
  cancelJob(
    input: {
      requestId: 15
    }) {
    result
  }
}

```

</details>

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
