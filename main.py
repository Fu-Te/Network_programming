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


#get_local_ip()
#get_global_ip()
#get_host_name()
#get_service_name(port=80,protocol_name='tcp')
get_service_name(port=25, protocol_name='tcp')
get_remote_ip(remote_host='www.google.com')