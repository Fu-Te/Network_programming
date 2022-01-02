# ネットワークプログラムを試すためのリポジトリ

RustとPythonを用いてsocat通信等を試していく．

# 注意事項
ポートスキャン等，不正アクセスにも使える技術が実装されているが，**決して第3者のサーバに対して実行しないようにしてください**．**不正アクセスの事前調査とみなされる可能性があります．
本リポジトリに存在するプログラムを利用し，不正アクセスに利用したとしても，本リポジトリ所有者は一切の責任を負いません．

# 免責
このリポジトリに存在するコードを利用し，いかなる不利益を被っても，本リポジトリの所有者は一切責任を負いません．

# Python

## tcp_scan.py
3wayhandshakeで接続し，開いているポートを特定します．
ログが残りやすい

## syn_scan.py
synパケットを投げて，syn+ackが帰って来ればポートが空いてる．
rst+ackが帰ってきたらポートは閉じている
ステルススキャン

## client.py & server.py
socket通信を用いたclient,serverモデル

## syn_scan.py
synパケットを投げる

## main.py
いろんな機能まとめたやつ

## 3way_handshake.py
3wayハンドシェイクを実現するクラス

## thread_port_scanner.py
socketを使ったポートスキャナー．実行速度が速い．
https://www.finddevguides.com/Python-penetration-testing-network-scanner
上記のサイトを参考