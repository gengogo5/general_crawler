module Mutations
  class UpdateCrawlRequest < BaseMutation
    # クロール種別ごとに必須パラメータが違う
    # 共通の更新ロジックは若干厳しいかもしれない
    # 実行中ジョブに影響する可能性もある
    # いったんCreateとDeleteだけで進める
  end
end
