# blog-markdown

ブログデータの保存用リポジトリです。

[このリポジトリ](https://github.com/Toshimichi0915/blog)がブログデータを定期的に読み込みウェブサイトが更新されます。

## 使い方

1. GitHubからpages/<ID>/contents.mdにブログの記事を書きます。
2. `python3 generate.py` を実行します。
3. ブログのタイトルとタグを半角スペース区切りで入力します。
4. `git push origin master` を実行します。

GitHubにデータがアップロードされるので、しばらく待つとウェブサイトが自動で更新されます。
  
