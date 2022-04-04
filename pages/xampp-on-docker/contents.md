# DockerでXAMPP環境を構築する

PHPの開発環境として名高いXAMPPですが、Dockerを使うことでインストールなしでお手軽にXAMPPを構築することができます。

## インストール手順

まずはじめに、

```
docker pull tomsik68/xampp
```

と入力してXAMPPのDocker Imageをpullします。pullが完了したら、プロジェクトを入れるディレクトリを作成してdocker-compose.ymlを作成します。

```yaml
version: "3"

services:
  main:
    image: tomsik68/xampp:8
    ports:
     - 3001:22
     - 3000:80
    volumes:
     - ./:/www
```

この内容でdocker-compose.ymlを保存したら、テストで表示するindex.phpを作成します。

```php
<?php
phpinfo();
```

これでプロジェクトの準備が整ったので、
```
docker-compose up -d
```
と入力してDocker Imageを立ち上げます。全てうまく行ったら、http://localhost:3000/www/index.php でウェブサイトが見れるようになります。

![image](https://user-images.githubusercontent.com/26406334/161461018-d2be2ea1-e226-4808-84d9-6c043e8b5e98.png)

## 注意点
* 3001番ポートにてSSH接続が可能です。ユーザー名、パスワードは共にrootです。
* PHPMyAdminは http://localhost:3000/phpmyadmin/ で接続可能です。
