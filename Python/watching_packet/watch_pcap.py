

from scapy.all import *
from datetime import datetime

# ----->　設定値ここから
PCAP_filename = "../pcap/sample.pcap"
SHOW_Detail = True
# <-----　設定値ここまで

# port番号を指定
def is_this_target_packet(packet):
    return TCP in packet and (packet[TCP].sport == 80 or packet[TCP].dport == 80)

def parse_pcap(filename, show_details):

    packets = rdpcap(filename)

    print("----------------------------------")
    target_cnt = 0
    for cnt, packet in enumerate(packets, 1):
        if is_this_target_packet(packet) == True:
            datetime_text = datetime.fromtimestamp(packet.time).isoformat()
            print("No:", cnt, " ", datetime_text, " ", packet.summary())
            target_cnt += 1
    print("target_cnt = ", target_cnt)
    print("----------------------------------")

    if show_details == False:
        return

    target_cnt = 0
    for cnt, packet in enumerate(packets, 1):
        if is_this_target_packet(packet) == True:
            datetime_text = datetime.fromtimestamp(packet.time).isoformat()
            print("No:", cnt, " ", datetime_text,
                  " TARGET_CNT", target_cnt, packet.summary())
            print("IP.len        = ", packet[IP].len)
            print("TCP.sport     = ", packet[TCP].sport)
            print("TCP.dport     = ", packet[TCP].dport)
            print("TCP.seq       = ", hex(packet[TCP].seq))
            print("TCP.ack       = ", hex(packet[TCP].ack))
            print("TCP.dataofs   = ", packet[TCP].dataofs)
            print("TCP.reserved  = ", packet[TCP].reserved)
            print("TCP.flags     = ", packet[TCP].flags)
            print("TCP.window    = ", packet[TCP].window)
            print("TCP.chksum    = ", packet[TCP].chksum)
            print("TCP.urgptr    = ", packet[TCP].urgptr)
            print("TCP.options   = ", packet[TCP].options)
            if Raw in packet:
                print("[RAW] ", packet[Raw])
                print("RAW:len = ", len(packet[Raw]))
            print("----------------------------------")
            target_cnt += 1

if __name__ == "__main__":

    parse_pcap(PCAP_filename, SHOW_Detail)

    print("completed.")
