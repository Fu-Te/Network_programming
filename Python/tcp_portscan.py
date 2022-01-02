import socket
import os

#ポートをスキャンするが，Synスキャンと比べるとログが残りやすい
#終わりのポート番号を探し，あいているところを探す．
ip = input("IPアドレスを入力:")
port = int(input('探索最初port番号を指定:'))
port_end = int(input("探索終端port番号を指定:"))

while port_end<port:
	print('最初と最後の数値が変')
	port = int(input('探索最初port番号を指定:'))
	port_end = int(input("探索終端port番号を指定:"))


open_port = []

while port <= port_end:
	s = socket.socket()
	errno = s.connect_ex((ip,port))
	s.close()

	if errno == 0:
		print('port {} is open',port)
		open_port.append(port)

	else:
		print("{} is close",port)
		print(os.strerror(errno))

	port = port + 1

print(open_port)