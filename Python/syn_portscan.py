from scapy.all import sr1, IP, TCP

ip = str(input("接続先IPを入力:"))
port_end = int(input("終端ポートを指定:"))

open_port = []
port = 0
ip = IP(dst=ip)

#syn+ackが帰って来ればポートが空いてる
#rst+ackが帰ってきたらポートは閉じている
#ステルススキャン

while port <= port_end:
	try:


		tcp = TCP(dport=port, flags='S')
		ret = sr1(ip/tcp, timeout=1, verbose=0)
		print("portnumber:{}",port)
		print('snd:{0:#010b}({1})'.format(bytes(tcp)[13],tcp.flags))
		print('rtn:{0:#010b}({1})'.format(bytes(ret['TCP'])[13],ret['TCP'].flags))

		open_flag = bytes(ret['TCP'])[13],ret['TCP'].flags
		
		if open_flag == '(20, <Flag 20 (RA)>)':
			continue
		else:
			open_port.append(port)

	except Exception as e:
		print("Exception:{0}".format(e))

	port = port+1

print(open_port)