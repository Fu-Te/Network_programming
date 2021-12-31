#ローカルipアドレスの取得
import socket
def get_local_ip():
	ip=socket.gethostbyname(socket.gethostname())
	print(ip)

#グローバルIPアドレスの取得
import urllib.request
def get_global_ip():
	ip = urllib.request.urlopen('http://ipcheck.ieserver.net').read().decode('utf-8')
	print(ip)
#ホスト名の取得
import socket
def get_host_name():
	host=socket.gethostname()
	print(host)


def get_service_name(port,protocol_name):
	print('Port',port)
	print('protocolname',protocol_name)
	print('Service Name:',socket.getservbyport(port,protocol_name))
	print('--------------')

def get_remote_ip(remote_host):
	print('Remote host name:',remote_host)
	print('Remote IP:',socket.gethostbyname(remote_host))
	print('---------------')

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


import subprocess

class Ping(object):
	def __init__(self,hosts):
		for host in hosts:
			#pingコマンド
			ping = subprocess.Popen(['ping','-c','1',host],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)

			#ping試験
			out,error=ping.communicate()

			#接続できなかったら
			if error:
				print('[NG]: ' +  host + ', Msg->\'' + error.rstrip() + '\'')

			#接続できたら
			else:
				print('[OK]:'+ host)



#get_local_ip()
#get_global_ip()
#get_host_name()
#get_service_name(port=80,protocol_name='tcp')
get_service_name(port=25, protocol_name='tcp')
get_remote_ip(remote_host='www.google.com')

#ping試験用ホスト
hosts = ['www.google.com','www.yahoo.jp']
Ping(hosts)
