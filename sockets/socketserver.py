import socket
import sys
from thread import *

HOST = ''
PORT = 8889
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('socket created')

try:
	s.bind((HOST,PORT))
except socket.error ,msg:
	print('Bind failed. Error Code:'+ str(msg[0])+' Message: '+msg[1])
	sys.exit()

print 'socket bind Complete'

s.listen(10)
print 'socket now listening'

def clientThread(conn):
	conn.send('welcome to the server. Type something and hit enter \n')

	while True:
		data= conn.recv(1024)
		reply = 'Ok..'+ data	
		if not data:
			break

		conn.sendall(reply)
	conn.close()

while 1:
	conn,addr= s.accept()
	print('Connected with '+ addr[0]+':'+str(addr[1]))

	start_new_thread(clientThread,(conn,))

s.close()	
