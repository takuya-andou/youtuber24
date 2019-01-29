# youtuber24_sample2
## 概要
[Docker上でSeleniumとHeadless ChromeとPython3を動かす](https://qiita.com/sikkim/items/447b72e6ec45849058cd)
こちらの記事を参考にSelenium/Chromeが動く環境を構築しました。

SeleniumとPythonを使い、Youtubeのコメント欄を監視しコメントを取得し続けるソースです。

## 事前準備
- Dockerをインストールして、dockerコマンドとdocker-composeコマンドが使用できるようにしてください。
- docker-compose.yml内のAPIKEYを書き換えてください。
- src/test_selenium.py が実行スクリプトですのでよしなに修正してください。

## 使い方
### 起動方法

```bash
$ docker-compose up -d
```

### 終了方法

```bash
$ docker-compose down
```

### VNC接続によるデバッグ
`VNC`で接続するとブラウザの動きを確認しながらデバッグすることができます。Docker環境のIPアドレスにVNC(デフォルトは5900番ポート)でアクセスした上で、サンプルスクリプトを実行してみてください。デフォルトのパスワードは"secret"です。
