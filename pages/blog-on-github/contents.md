# GitHub上でブログをホスティングする方法

このブログのコンテンツは[GitHubのリポジトリ](https://github.com/Toshimichi0915/blog-markdown)でホスティングされているのですが、その仕組みとしてはNext.jsのStatic Site Generationを用いて5分毎にGitHubから最新の情報を取得してサイトを更新しています。

またNext.jsのアプリケーションはVercelの無料プランでホスティングしています。この方法であればすべて無料でブログを作成できる上、ブログ文章の作成もGitHub上で行えます。画像のアップロード・管理も全てGitHubが自動で行ってくれるのでまさしく天国といった感じです。

では早速、GitHub上でブログをホスティングする方法を書いていこうと思います。

## ブログコンテンツのリポジトリを作成する

GitHub上でブログのコンテンツを書き込むリポジトリを作成してください。そのリポジトリの構成は以下のようにしてください。

* pages - 記事を入れるディレクトリ
* index.json - 全ての記事のインデックス

pagesディレクトリで好きな内容の記事を書いたら、index.jsonに以下の内容を書き込みます。

```json
{
    "pagesディレクトリのファイル名": {
        "name": "記事の見出し",
        "tags": ["タグ1", "タグ2"],
        "date": 1648664352
    }
}
```

dateにはブログを記事を書いた時刻（UTC、Epoch秒）を指定してください。


## 2. アプリケーションの[リポジトリ](https://github.com/Toshimichi0915/blog)をフォークする

[このURL](https://github.com/Toshimichi0915/blog)からソースコードをフォークしてください。その次にリポジトリのURLがcore/posts.jsに書かれているので、自分のリポジトリのURLに書き換えてください。またpages/components/navbar.jsにはナビゲーションバーがあるので、ナビゲーションバーも自分のお好みで変更してください。

### 3. Vercelにアップロードする

Vercelでは無料でNext.jsのアプリケーションをホスティングできるので、Vercelのアカウントを作って2で作ったアプリケーションをデプロイします。

![image](https://user-images.githubusercontent.com/26406334/160891564-8cf1d4d4-2b43-4be2-bb09-de7b02e8f299.png)

アカウントを作ったら右上のNew projectからImport Git Repositoryを選択してブログのリポジトリを指定してください。もしリポジトリが表示されない場合はおそらくVercelとGitHubアカウントが連携されていないと思われるので、Add GitHub AccountからGitHubアカウントを追加してください。これだけでデプロイは完了です！

後はお好みでドメインを設定してあげれば完成となります。

### 最後に

いかがだったでしょうか。もしこの方法でブログを作成された方がいれば、GitHubでstarとフォローをお願いします。
