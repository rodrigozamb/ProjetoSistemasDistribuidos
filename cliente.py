
#client.py

#!/usr/bin/python                      # This is client.py file

import socket                          # Import socket module


packageSize = 1024                     # Size of package to send or receive

s = socket.socket()                    # Create a socket object
host = socket.gethostname()            # Get local machine name
port = 12345                           # Reserve a port for your service.

s.connect((host, port))

flag = True

while flag:
	
	msg = input("Digite mensagem: ")
	s.send(msg.encode())

	if msg == "SAIR":
		break

	if msg == "1":
		print("Digite a chave e valor separados por vírgula ( ex: '1,lala' ) ")
		insertData = input()
		s.send(insertData.encode())
	elif msg == 2:
		print("Listando dados:")
		
	data = s.recv(1024)
	print("Mensagem recebida: ",data.decode())


print("Desconectando Client...")
s.close()    