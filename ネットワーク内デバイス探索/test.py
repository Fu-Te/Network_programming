from socket import timeout
from scapy.all import *
import subprocess as sbp

def get_addr(network_part):
    # ICMPパケットを流して結果を1つだけ受け取る dstの後をブロードキャストアドレスにしたいところ
    # ネットワーク部だけ入力してもらって，後は繰り返す？ 192.168.1.0~192.168.1.254みたいに．
    #broadcast_ipaddr = 
    receives_ICMP = []
    receives_ARP = []
    ip_addr_list = []
    for i in range (0,9):
        i = str(i)
        dst_addr = network_part + i
        ip_addr_list.append(dst_addr)
        
        print('現在探索中のアドレスは{}'.format(dst_addr))
        
        frame = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op=1, pdst = dst_addr)
        receive = srp1(frame,timeout=3,iface='en0')
        try:
            receives_ARP.append(receive[Ether].src)
        except:
            receives_ARP.append(receive)
        
        
        
    print(ip_addr_list)
    print(receives_ARP)
    print(receives_ICMP)
    #return results
    
get_addr('192.168.10.')