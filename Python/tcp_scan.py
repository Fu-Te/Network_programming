import socket
import os

#ポートをスキャンするが，Synスキャンと比べるとログが残りやすい

s = socket.socket()
errno = s.connect_ex(('192.168.1.9',80))
s.close()

if errno == 0:
	print('port is open')

else:
	print(os.strerror(errno))