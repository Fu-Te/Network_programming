import socket

server = 'www.google.com'
port = 80

# Getting Server IP
# server_ip = socket.gethostbyname(server)
# print(server_ip)

request = 'GET / HTTP/1.1\nHOST: ' + server + '\n\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
s.send(request.encode())

result = s.recv(1024)
print (result)