# IntelliJで発生するGradle Syncの問題

## 問題の発生

GitHubからリポジトリをクローンしてGradleのプロジェクトをIntelliJで開いたところ、突如として次のようなエラーメッセージが表示されました。
![image](https://user-images.githubusercontent.com/26406334/161318544-61d3829c-ba94-4154-9969-1f7cd300231c.png)

```
Could not resolve spigot-api-1.18.2.-R0.1-SNAPSHOT.jar
```

GradleではうまくビルドできるのにIntelliJでは上手くいかない謎のエラーが発生し、頭を悩ませる事態に。

調べてみたところ、Gradleのキャッシュが悪さをしているとのこと。 %USERPROFILE%/.gradle/caches ディレクトリを消去してキャッシュをクリアすることで正常に戻りました。

## 問題の解決方法

まずキャッシュをクリアする前に、念のためIntelliJを閉じておきます。

次に、Win + Rを同時に押すと実行ウインドウが出てくるので、

```
%USERPROFILE%/.gradle
```

と入力してエンターを押します。

![image](https://user-images.githubusercontent.com/26406334/161319252-a7b7e86d-f42a-4aa7-a85b-14215c1e6882.png)

エクスプローラーが開くので、cacheディレクトリを消去しましょう。もし「別のプロセスが使用しています」と表示されてファイルを消せない場合は、Resource Monitorからプロセスを特定してkillしてください。
