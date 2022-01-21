from scapy.all import *

def get_mac(ip_address):
    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2, retry=10)
    for s, r in responses:
        return r[Ether].src
    return None

ip = '127.0.0.1'
get_mac(ip)