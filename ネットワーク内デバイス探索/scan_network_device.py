from scapy.all import *
import subprocess as sbp

# ICMPパケットを送って，返信させてIPアドレスを特定する

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
def broadcastaddr(network_part):
    # ICMPパケットを流して結果を1つだけ受け取る dstの後をブロードキャストアドレスにしたいところ
    # ネットワーク部だけ入力してもらって，後は繰り返す？ 192.168.1.0~192.168.1.254みたいに．
    #broadcast_ipaddr = 
    receives_ICMP = []
    receives_ARP = []
    for i in range (1,10):
        i = str(i)
        dst_addr = network_part + i
        
        print('現在探索中のアドレスは{}'.format(dst_addr))
        
        #results = srp1(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op=1,pdst=dst_addr))
        results = sr1(IP(dst = dst_addr)/ICMP(),timeout = 1)
        receives_ICMP.append(results)
        
        results = sr1(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op=1, pdst = dst_addr),timeout = 3)
        receives_ARP.append(results)
        
        
    
    print(receives_ARP)
    print(receives_ICMP)
    #return results

# arp
def get_macaddr():
    packet = ARP()


# hostname
def get_hostname():
    packet = ip()
    
if __name__ == '__main__':
    network_part = get_network_part('192.168.1.1')
    print(broadcastaddr(network_part))