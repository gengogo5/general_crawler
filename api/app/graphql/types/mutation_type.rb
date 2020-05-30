module Types
  class MutationType < Types::BaseObject
    field :delete_crawl_request, mutation: Mutations::DeleteCrawlRequest
    field :update_crawl_request, mutation: Mutations::UpdateCrawlRequest
    field :create_crawl_request, mutation: Mutations::CreateCrawlRequest
    # TODO: remove me
    field :test_field, String, null: false,
      description: "An example field added by the generator"
    def test_field
      "Hello World"
    end
  end
end
