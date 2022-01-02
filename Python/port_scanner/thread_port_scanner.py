import socket
import time
import threading

from queue import Queue
socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

target = input('スキャンするIPアドレスを指定: ')
port = int(input('スキャンを開始するポート番号を指定:'))
port_end = int(input('スキャンを終了するポートを指定:'))


t_IP = socket.gethostbyname(target)
print ('Starting scan on host: ', t_IP)

def portscan(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		con = s.connect((t_IP, port))
		with print_lock:
			print(port, 'is open')
		con.close()
	except:
		pass

def threader():
	while True:
		worker = q.get()
		portscan(worker)
		q.task_done()

q = Queue()
startTime = time.time()

for x in range(100):
	t = threading.Thread(target = threader)
	t.daemon = True
	t.start()

for worker in range(port,port_end):
	q.put(worker)

q.join()
print('Time taken:', time.time() - startTime)
