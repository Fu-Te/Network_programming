from scapy.all import *
import threading

class SendPacket(threading.Thread):
    def __init__(self,src_ip,dst_ip,src_port,dst_port,file_size):
        self.src_ip=src_ip
        self.dst_ip=dst_ip
        self.src_port=src_port
        self.dst_port=dst_port
        self.file_size=file_size
        
        self.stop_event=threading.Event()
        self.thread=threading.Thread(target=self.run)
        self.thread.start()
        
    def run(self):
        
    
    
    def make_packet():
        ip=IP(src='1.2.3.4',dst='192.168.1.120')
        tcp=TCP(sport=22222,dport=80,flags='S')
        raw=Raw(b'X'*1024)
        packet=ip/tcp/raw
        return packet



packet = ip/tcp/raw
send(packet,count=5)