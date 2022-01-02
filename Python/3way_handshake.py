from scapy.all import *


class TCP_CONNECT:
	def __init__(self,
				src = '127.0.0.1',
				dst = '127.0.0.1',
				sport = 60000,
				dport = 60000):
		self.src = src
		self.dst = dst
		self.sport = sport
		self.dport = dport
		self.ip = IP(dst = self.dst)
		self.tcp = TCP(sport = self.sport , dport = self.dport , flags = 'S', seq = 100)


	def synchronize(self):
		
		# send syn get ack
		syn = self.ip / self.tcp
		self.syn_ack = sr1(syn)


		# send syn

		self.tcp.seq = self.tcp.seq +1
		self.tcp.ack = self.syn_ack.seq
		self.tcp.flags = 'A'
		ack = self.ip / self.tcp

		send(ack)

		return syn, self.syn_ack, ack


	def fin(self):

		#send FIN
		self.tcp.seq
		fin = self.ip / TCP(sport = self.sport, dport = self.dport, flags = 'FA', seq = self.syn_ack.ack, ack = self.syn_ack.seq +1)
		self.fin_ack = sr1(fin)

		#return final ack
		lastack = self.ip / TCP(sport = self.sport, dport = self.dport, flags = 'A', seq = self.fin_ack.ack, ack = self.fin_ack.seq +1)
		send(lastack) 

	def __del__(self):
		self.fin()


tcp_connect = TCP_CONNECT(src = '192.168.1.9',dst = '192.168.1.6',sport = '54321',dport = 80)
tcp_connect.synchronize()

tcp_connect.fin()