class CreateArticleArchives < ActiveRecord::Migration[5.2]
  def change
    create_table :article_archives do |t|
      t.text :url
      t.binary :content, :limit => 15.megabytes
      t.string :title

      t.timestamps
    end
  end
end
