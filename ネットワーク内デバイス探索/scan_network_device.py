from socket import timeout
from scapy.all import *
import subprocess as sbp
import netifaces
import socket


#自身のIPアドレスを取得する
def get_own_ip():
    ip = netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']
    return ip


# IPアドレスのネットワーク部を特定する．
def get_network_part(my_ipaddr):
    #自身のIPアドレスを取得する方法があれば，それを使った方がユーザからの入力を待たなくていいので，いいかもしれない．　s
    #自身のIPアドレスとサブネットマスクからブロードキャストアドレスを求める．
    #/24,/16に対応するため（ネットワーク部を指定できるように）に要改善．
    count = 0
    my_ip = []
    network_part = ''
    
    for string in my_ipaddr:
        if string == '.':
            count = count + 1
            my_ip.append(string)
            if count == 3:
                break
        else:
            my_ip.append(string)
        
    for i in my_ip:
        network_part = network_part + i
    
    print(network_part)
    return network_part

# ICMPでブロードキャストを流し，返答を受け取ることで各種アドレスを特定
def get_addr(network_part):
    # ICMPパケットを流して結果を1つだけ受け取る dstの後をブロードキャストアドレスにしたいところ
    # ネットワーク部だけ入力してもらって，後は繰り返す？ 192.168.1.0~192.168.1.254みたいに．
    #broadcast_ipaddr = 
    receives_ICMP = []
    receives_ARP = []
    ip_addr_list = []
    for i in range (0,3):
        i = str(i)
        dst_addr = network_part + i
        ip_addr_list.append(dst_addr)
        
        print('現在探索中のアドレスは{}'.format(dst_addr))
        
        
        frame = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op=1, pdst = dst_addr)
        receive = srp1(frame,timeout=1,iface='en0')
        try:
            receives_ARP.append(receive[Ether].src)
        except:
            receives_ARP.append(receive)
        
    return ip_addr_list,receives_ARP

# arp



# hostname
def get_hostname(ip_list):
    host_list = []
    for ip in ip_list:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            host_list.append(hostname)
        except:
            host_list.append('None')
    return host_list
    
if __name__ == '__main__':
    own_ip = get_own_ip()
    network_part = get_network_part(own_ip)
    ip_addr_list,mac_addr_list =get_addr(network_part)
    host_list = get_hostname(ip_addr_list)
    
    print('ip:{}'.format(ip_addr_list))
    print('mac:{}'.format(mac_addr_list))
    print('hostname:{}'.format(host_list))