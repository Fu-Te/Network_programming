from scapy.all import *



packet = IP(src='1.2.3.4',dst='192.168.1.120')/TCP(sport=22222,dport=80,flags='S')
send(packet,count=5)