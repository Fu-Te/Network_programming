# ネットワーク系の学習のためのリポジトリ．
ネットワーク分野に興味があるので，プログラム言語を使って様々なことをしてみたい，ネットワークを用いてなにか作りたいという思いから，プログラミングをしながらネットワークを学習したい．

IBM資料の検索欄でコマンド名を入力すると詳細なデータが出てくる．
IBM資料: https://www.ibm.com/docs/ja/aix/7.2?topic=networking

ソケットで相手のpcと接続して，そこでosを使ってファイルパス等の確認をする．
ファイルを確認したら，重要なデータが入ってそうなファイルの取得を試みる．

# 注意事項(Warning)
このレポジトリに存在するプログラムファイルは，許可されたネットワーク，対象にのみ使用するようにしてください．
何かしらのトラブル等に関して，本レポジトリ所有者は責任は一切所有しません．

The program files in this repository should be used only on authorized networks and for authorized host.
The owner of this repository assumes no responsibility for any problems that may arise.


# dockerを用意してあります
dockerを利用する場合は，
```cd docker/python-docker```
```docker compose up -d --build```
で作成が可能です．

# 必要なライブラリ
socat scapy subprocess ipaddress
```
pip install socat scapy
```
でライブラリを入れ，コードを実行してください．

python3.9.7で動作確認

# Ethernet
Macアドレスを使う．
イーサネットでの役割・・・近隣までの荷物の配達
送信元・宛先MACアドレスは，ルータを通過すると異なる．違うセグメントにIPがあるときは，そこのセグメントに行けるルータのMACアドレスが宛先となり送信元はデータを送信したホストのMACアドレス，そのルータから目的のホストに届けるときは，送信元がルータのMACアドレスになり宛先がホストのMACアドレスになる．


## arp
参考：http://win.kororo.jp/archi/tcp_ip/arp_rarp.php

arpはIPv4のときにもちいられる．
IPアドレスを持った相手とイーサネットで通信するには，相手のMACアドレスを知っている必要がある．
宛先のMACアドレスをff:ff:ff:ff:ff:ffとし，パケットを送信することで，Macアドレスを返してもらえる．
送信元MACアドレスを偽装することでなりすましも可能
```$ arp -a```

## rarp
参考：http://win.kororo.jp/archi/tcp_ip/arp_rarp.php


MACアドレスからIPアドレスの情報を取得できる．
自分のIPアドレスがわからない時などに，使ったりする．


IPv6の場合はICMPv6の近傍探索が使われる．




# IP
IPアドレスを使う．
これらのコマンドではICMPプロトコルが内部的に使われている．ICMPは通信で生じたエラーの通知など様々な用途で用いられる．
ICMPのエコーリクエスト(Echo request)とエコーリプライ(Echo reply)というメッセージをやりとりする．

マニュアル（オプションについて知りたい時）は```$ man [command name]```

## ping
TCP/IPのネットワーク疎通を確認する．
```$ ping 192.168.1.1```
なんらかのエラーが表示されるか応答に対応する表示がないときは
1.通信環境に影響があり，パケットが破棄された
2.インターネットに接続できていない
3.宛先あるいは経路にICMPのメッセージを破棄するネットワークが存在する．

## tcpdump
コンピュータの中を流れる通信を覗き見できる．（パケットキャプチャ，スニッフィング）

[参考](https://xtech.nikkei.com/it/article/COLUMN/20140512/556024/)

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

## traceroute
[参考](https://atmarkit.itmedia.co.jp/ait/articles/0108/30/news003.html)
パケットがどのような道順を通って目的地まで届くのかを確認できる．
ネットワークのトラブルシューティングでよく使われる．
```$ traceroute -n 192.168.1.1```

IPプロトコルのTTL（TimeToLive）フィールドを使う．TTLを1つずつ増やし，目的地まで送る．そうすることで，パケットを破棄した経路状のルータから，ICMPの時間切れメッセージが返ってきて，そのメッセージには送信元IP（ルータのIPアドレス）がある．時間切れメッセージを送ってきたルータを並べることで経路を調べられる．

## ip route show
参考1:https://www.ibm.com/docs/ja/power7?topic=commands-netstat-command


ルーティングテーブルの確認をする
Linux ```$ ip route show ```
mac ```$netstat -rn```
ルーティングテーブルはノードがそれぞれ保持している．
Defaultはデフォルトルート
192.168.10.1/32・・・/32のような書き方はIPアドレスをまとめて宛先として指定している．

実行結果↓
```
default via 192.168.10.1 dev wlan0 proto dhcp src 192.168.10.8 metric 304 
169.254.0.0/16 dev usb0 scope link src 169.254.234.178 metric 203 
192.168.10.0/24 dev wlan0 proto dhcp scope link src 192.168.10.8 metric 304 
```

# TCP
## nmap
nmapコマンドを使ってポートスキャンをすることもできる．

```
$ nmap -sT -p 1-65535 ipaddr
```
オプションに-sAをつけるとファイアウォールの有無を調べられる
```
$ nmap -sA ipaddr
```
相手のOSを調べる
```
$ nmap -O ipaddr
```




# 用語
ルータ・・・別のルータまたはホストから送られてきたパケットを次のルータ，ホストに送る機器のこと．セグメント同士の橋渡しを行う．
ホスト・・・ルータではないコンピュータのこと
ノード・・・ネットワークにつながったコンピュータの総称
デフォルトルート・・・デフォルトルートとは、コンピュータネットワークのルーティングテーブルにおいて、全ての宛先を示す特殊な経路情報
セグメント・・・なんらかの基準により分割した物理的なネットワーク断片
サブネットマスク・・・ネットワーク部を1に，ホスト部を0にした32ビットの整数．これをIPアドレスのビット列とAND演算するとネットワークアドレスを取り出せる．
MACアドレス・・・48ビットの整数．一意な識別子．上位24ビット→ベンダー，下位24ビット→ベンダーが割り当てる数字．
ルータ・・・ネットワーク層でパケットを転送する機器
ブリッジ・・・データリンク層でフレームを転送する機器のこと．

IPv4アドレス・・・32ビット(2の32乗)で表される．1か0が32個連なるが，人には分かりにくいので，それぞれ8ビットごとに区切り，さらにその数字を10進数を使って表すことによって分かりやすくしている．例↓
00000000000000000000000000000000
↓
00000000.00000000.00000000.00000000
↓
192.10.10.1
IPv4アドレスは2つの部分に分かれている→ネットワーク部とホスト部
ネットワーク部はセグメントを表し，ホスト部はホストを表す．→ネットワーク部が同じなら同じセグメント
前半24ビットがネットワーク部，後半8ビットがホスト部を表す．
192.10.10(ネット部).1(ホスト部)
192.10.10.0/24→ネットワーク部は24ビット目で分けるということを表している．→CIDR表記
192.10.10.0/24→デフォルトゲート(0.0.0.0/0)



# Network Namespace
参考：https://hawksnowlog.blogspot.com/2021/05/getting-started-network-namespace.html


Network Namespace
Natwork Namespaceを作る
```$ sudo ip netns add [name]```
Network Namespaceを確認する
```$ ip netns list```
Network Namespaceの環境でIPアドレスを確認する
```$ ip address show```
```$ sudo ip netns exec [filename] ip address show```
NetworkNamespaceは再起動されると消える．

Network Namaspaceの環境をつかってシェルを起動できる
```$ sudo ip netns exec [name] bash```




Network Namespaceを使うと，ネットワーク的にはシステムから独立した領域を作れ，別にLinuxをインストールしたマシンを用意したように見える．

# Error
以下のエラーに悩まされているところである

        PIP package scapy-python3 used to provide scapy3k, which was a fork from scapy implementing python3 compatibility since 2016. This package was included in some of the Linux distros under name of python3-scapy. Starting from scapy version 2.4 (released in March, 2018) mainstream scapy supports python3. To reduce any confusion scapy3k was renamed to kamene. 
You should use either pip package kamene for scapy3k (see http://github.com/phaethon/kamene for differences in use) or mainstream scapy (pip package scapy, http://github.com/secdev/scapy).  

Traceback (most recent call last):
  File "/opt/homebrew/bin/scapy", line 8, in <module>
    sys.exit(interact())
  File "/opt/homebrew/lib/python3.9/site-packages/scapy/main.py", line 550, in interact
    SESSION, GLOBKEYS = init_session(session_name, mydict)
  File "/opt/homebrew/lib/python3.9/site-packages/scapy/main.py", line 411, in init_session
    importlib.import_module(".all", "scapy").__dict__
  File "/opt/homebrew/Cellar/python@3.9/3.9.10/Frameworks/Python.framework/Versions/3.9/lib/python3.9/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1030, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1007, in _find_and_load
  File "<frozen importlib._bootstrap>", line 986, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 680, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 850, in exec_module
  File "<frozen importlib._bootstrap>", line 228, in _call_with_frames_removed
  File "/opt/homebrew/lib/python3.9/site-packages/scapy/all.py", line 5, in <module>
    raise Exception(msg)
Exception: 
        PIP package scapy-python3 used to provide scapy3k, which was a fork from scapy implementing python3 compatibility since 2016. This package was included in some of the Linux distros under name of python3-scapy. Starting from scapy version 2.4 (released in March, 2018) mainstream scapy supports python3. To reduce any confusion scapy3k was renamed to kamene. 
You should use either pip package kamene for scapy3k (see http://github.com/phaethon/kamene for differences in use) or mainstream scapy (pip package scapy, http://github.com/secdev/scapy).  