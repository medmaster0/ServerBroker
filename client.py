import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect(('192.168.0.4', 5555)
	#s.send(b"hell")
	#data = s.recv(1024)

#print(repr(data))