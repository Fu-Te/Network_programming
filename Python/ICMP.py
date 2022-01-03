from scapy.all import *

# ICMPパケット送信
target_ip = input('対象のIPアドレスを入力:')

frame = Ether() / IP(dst=target_ip)/ICMP()
send(frame)