module Types
  class QueryType < Types::BaseObject
    # Add root-level fields here.
    # They will be entry points for queries on your schema.

    field :requests, [Types::CrawlRequestType ], null: false, description: 'クロール要求を全件取得する'
    def requests
      CrawlRequest.all
    end
  end
end
