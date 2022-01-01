import re
import telnetlib

HOST = '' # your server
user = '' # username
password = '' # password

tn = telnetlib.Telnet(HOST)

tn.read_until('login: ')
tn.write(user+ '\n')

if password:
	tn.read_until('Password: ')
	tn.write(password + '\n')

tn.write('ls -al\n')
tn.write('exit\n')

result = tn.read_all()



r = re.compile(r'\x1b\[.*?m\[?')
result1 = re.sub(r,'',result)


result2 = result1.decode('utf-8').encode('cp932')

print(result2)