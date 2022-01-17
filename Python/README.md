# ネットワーク系の学習のためのリポジトリ．
ネットワーク分野に興味があるので，プログラム言語を使って様々なことをしてみたい，ネットワークを用いてなにか作りたいという思いから，プログラミングをしながらネットワークを学習したい．

ソケットで相手のpcと接続して，そこでosを使ってファイルパス等の確認をする．
ファイルを確認したら，重要なデータが入ってそうなファイルの取得を試みる．


# 必要なライブラリ
socat scapy
```
pip install socat scapy
```
でライブラリを入れ，コードを実行してください．

python3.9.7で動作確認

# Command
これらのコマンドではICMPプロトコルが内部的に使われている．ICMPは通信で生じたエラーの通知など様々な用途で用いられる．
ICMPのエコーリクエスト(Echo request)とエコーリプライ(Echo reply)というメッセージをやりとりする．
## ping
TCP/IPのネットワーク疎通を確認する．
```$ ping 192.168.1.1```
なんらかのエラーが表示されるか応答に対応する表示がないときは
1.通信環境に影響があり，パケットが破棄された
2.インターネットに接続できていない
3.宛先あるいは経路にICMPのメッセージを破棄するネットワークが存在する．

## tcpdump
コンピュータの中を流れる通信を覗き見できる．（パケットキャプチャ，スニッフィング）

[参考](https://qiita.com/tossh/items/4cd33693965ef231bd2a)

1.すべてのインターフェースをキャプチャする```$ sudo tcpdump ```
2.ASCIIで見たい時```$ sudo tcpdump -A```
3.インターフェースを指定```$ sudo tcpdump -i [interface]```
4.[filename]で指定したファイルに結果を出力```$ sudo tcpdump -w [filename]```
5.tcpdumpでとったキャプチャ結果を読み込む```$ sudo tcpdump -r [filename]```
6.自ホスト宛以外のデータはキャプチャしない```$ sudo tcpdump -p```
7.送信元ipアドレスを指定```$ tcpdump src host [src_ip]```
8.送信先ipアドレスを指定```$ tcpdump dst host [dst_ip]```
9.送信元もしくは送信先にipアドレスを指定```$ tcpdump host [target_ip]```
10.送信元もしくは送信先にipアドレスレンジを指定```$tcpdump net [dst_net] mask [net_mask]```
11.送信元ipアドレスレンジを指定```tcpdump src net [src_net] mask [net_mask]```
12.送信先ipアドレスレンジを指定```tcpdump dst net [dst_net] mask [net_mask]```
13.送信元ポート番号を指定```tcpdump src port [port]```
14.送信先ポート番号を指定```tcpdump dst port [port]```
15.送信先もしくは送信元ポート番号を指定```tcpdump port [port]```
それぞれの条件をandやorで繋ぐこともできる．
ex```tcpdump port 80 and host 192.168.1.1```
