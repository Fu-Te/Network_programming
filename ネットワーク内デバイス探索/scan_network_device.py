from scapy.all import *
import subprocess as sbp

# ICMPパケットを送って，返信させてIPアドレスを特定する
def get_ipaddr(my_ipaddr):
    #自身のIPアドレスとサブネットマスクからブロードキャストアドレスを求める．
    count = 0
    my_ip = []
    for string in my_ipaddr:
        if string == '.':
            count = count + 1
            my_ip.append(string)
            if count == 3:
                break
        else:
            my_ip.append(string)
        
    print(my_ip)

# ICMPでブロードキャストを流し，返答を受け取ることで各種アドレスを特定
def broadcastaddr():
    # ICMPパケットを流して結果を1つだけ受け取る dstの後をブロードキャストアドレスにしたいところ
    # ネットワーク部だけ入力してもらって，後は繰り返す？ 192.168.1.0~192.168.1.254みたいに．
    broadcast_ipaddr = 
    for i in range (0,255):
        receives = []
        packets = srp1(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op=1,pdst=))
        receives.append(packets)

# arp
def get_macaddr():
    packet = ARP()


# hostname
def get_hostname():
    packet = ip()
    
if __name__ == '__main__':
    broadcastaddr()