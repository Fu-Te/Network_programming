import threading
from scapy.all import *

class SniffRecPkt(threading.Thread):
    def __init__(self,target_ip):
        super(RecPingScan, self).__init__()
        self.target_ip = target_ip
        self.stop_event = threading.Event() #停止させるかのフラグ
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

    def run(self):
        while not self.stop_event.is_set():
            sniff(filter="tcp and ip src host " + self.target_ip,prn=packet_show, count=1)

    def stop(self):
        """スレッドを停止させる"""
        self.stop_event.set()
        self.thread.join()    #スレッドが停止するのを待つ


def packet_show(packet):
    if packet[TCP].flags==18: #SYN/ACKパケットだった時のみ
        print("IP : " + str(packet[IP].src) + " | TCP PORT : " + str(packet[TCP].sport))

if __name__ == '__main__':
    target_ip = "192.168.1.1"
    Rec_thread=SniffRecPkt(target_ip)

    target_ip="192.168.1.1"
    dst_port = 5001
    src_port = 5002
    frame = IP(dst=target_ip)/TCP(flags = 'S',sport=src_port,dport=dst_port)
    send(frame)

    Rec_thread.stop()
