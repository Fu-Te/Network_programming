import socket
import os
from tqdm import tqdm

#ポートをスキャンするが，Synスキャンと比べるとログが残りやすい
#終わりのポート番号を探し，あいているところを探す．
ip = input("IPアドレスを入力:")
port = int(input('探索最初port番号を指定(0以上):'))
port_end = int(input("探索終端port番号を指定(65535以下):"))

while port_end<port:
	print('最初と最後の数値が変')
	port = int(input('探索最初port番号を指定(0以上):'))
	port_end = int(input("探索終端port番号を指定(65535以下):"))


open_port = []

# 指定したポート番号内とIPアドレスで開いているポートを探す．

for port in tqdm(range(port,port_end+1)):
	s = socket.socket()
	errno = s.connect_ex((ip,port))
	s.close()

	if errno == 0:
		print('port {} is open',port)
		open_port.append(port)

	else:
		print("{} is close",port)
		print(os.strerror(errno))

	

print(open_port)