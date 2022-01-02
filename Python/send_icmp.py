from scapy.all import *

pkt = IP(dst='www.google.com')/ICMP()

print(pkt.show())

sr1(pkt)


