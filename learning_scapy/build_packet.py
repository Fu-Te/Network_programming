# パケットを作る
packet = IP(dst = '192.168.1.9')/ICMP(type=8)

#パケットを送る
send(packet)