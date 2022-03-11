from scapy.all import *
import threading

class SendPacket(threading.Thread):
    def __init__(self,src_ip,dst_ip,src_port,dst_port,file_size,sending_count):
        self.src_ip=src_ip
        self.dst_ip=dst_ip
        self.src_port=src_port
        self.dst_port=dst_port
        self.file_size=file_size
        self.sending_count=sending_count
        
        
        self.stop_event=threading.Event()
        self.thread=threading.Thread(target=self.run)
        self.thread.start()
        
        
    def __make_packet(self,src_ip,dst_ip,src_port,dst_port,file_size):
        ip=IP(src=src_ip,dst=dst_ip)
        tcp=TCP(sport=src_port,dport=dst_port,flags='S')
        raw=Raw(b'X'*file_size)
        packet=ip/tcp/raw
        return packet
    
    def __sending_packet(self,packet,sending_count):
        a=a
    
    def run(self):
        packet=make_packet()
        
        while not self.stop_event.is_set():
            sending_packet()
            
        
    def stop(self):
        self.stop_event.set()
        self.thread.join()
        
        
    
    
    
    def make_packet(self):
        ip=IP(src='1.2.3.4',dst='192.168.1.120')
        tcp=TCP(sport=22222,dport=80,flags='S')
        raw=Raw(b'X'*1024)
        packet=ip/tcp/raw
        return packet



packet = ip/tcp/raw
send(packet,count=5)



#入力
src_ip='1.2.3.4'
dst_ip='192.168.1.120'
src_port=12345
dst_port=80
filesize=1024
sending_count=5


send=SendPacket(src_ip,dst_ip,src_port,dst_port,filesize,sending_count)
send.make_packet()
