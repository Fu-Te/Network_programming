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
print ("Content-Type: text/html\n")

import urllib.request as urllib2
import json
import codecs

#API base url,you can also use https if you need
url = "http://macvendors.co/api/"
#Mac address to lookup vendor from
mac_address = "BC:92:6B:A0:00:01"

request = urllib2.Request(url+mac_address, headers={'User-Agent' : "API Browser"}) 
response = urllib2.urlopen( request )
#Fix: json object must be str, not 'bytes'
reader = codecs.getreader("utf-8")
obj = json.load(reader(response))

#Print company name
print (obj['result']['company']+"<br/>")

#print company address
print (obj['result']['address'])