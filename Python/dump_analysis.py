from scapy.all import *
from datetime import datetime

def analyze(pkt):
    # キャプチャ日時はpkt.timeからunix timestampで得られる
    datetime_str = datetime.fromtimestamp(pkt.time).isoformat()
    return "[%s] %s" % (datetime_str, pkt.summary())

# offline: 読み込むpcapファイルを指定
# filter: BPF形式でフィルタリングルールを指定
# store: 0を指定することで、読み終わったパケットは捨てられ、逐次的に解析できる
# prn: 個々のパケットを引数として関数を呼び出し、その戻り値を標準出力に吐く
sniff(offline="test.pcap", filter="icmp", store=0, prn=analyze)