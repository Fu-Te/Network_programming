from scapy.all import *

sr1(IP(dst='www.google.com')/TCP(dport=80,flags='S'))
