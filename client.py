import socket

def send_tcp():
	soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	soc.connect(('localhost',50007))

	while(1):
		data=soc.recv(1024)
		print('Server>',data)
		data=input('Client>')
		soc.send(data)

		if data=="q":
			soc.close()
			break

send_tcp()
