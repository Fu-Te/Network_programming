from scapy.all import *

ip=IP(src='1.2.3.4',dst='192.168.1.120')
tcp=TCP(sport=22222,dport=80,flags='S')
raw=Raw(b'X'*1024)

packet = ip/tcp/raw
send(packet,count=5)