import socket


def receive_tcp():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(('localhost',50007)) #指定したホストとポートをソケットに設定
	s.listen(1) #1つの接続要求を待つ
	soc,addr=s.accept() #要求が車でブロック
	print('Connected by'+str(addr))

	while(1):
		data=input('Server>') #入力待機（サーバ側）
		soc.send(data) #ソケットにデータを送信
		data=soc.recv(1024) #データを受信1024バイト
		print('Client>',data) #サーバ側の読み書きを表示

		if data=='q': #qが押されたら終了
			soc.close()
			break

receive_tcp()