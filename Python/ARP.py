from scapy.all import *

# arpリクエストメッセージ送信
target_ip = input('対象ipアドレス:')

frame = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op=1, pdst = target_ip)
print(srp1(frame))