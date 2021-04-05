#server.py
#!/usr/bin/python                           # This is server.py file

import socket                               # Import socket module
import threading

packageSize = 1024  

s = socket.socket()                         # Create a socket object
# host = socket.gethostname()                 # Get local machine name
host = ''                 # Get local machine name
port = 12345                                # Reserve a port for your service.
s.bind((host, port))                        # Bind to the port

database = dict([])

def handle_client(c, addr):
	global database
	print('Got connection from', addr)
	flag = True

	try:
		while flag:
			data = c.recv(1024)
			messageDecoded = data.decode()
			print("["+str(addr)+"] Mensagem recebida: "+messageDecoded)
			if messageDecoded == "SAIR":
				flag = False

			if messageDecoded == "1":
				# adicionar
				idata = c.recv(1024)
				insertData = idata.decode()
				insertData = insertData.split(",")
				# c.send("Operation success".encode())

				if len(insertData) == 2:
					database[insertData[0]] = (1,"td",insertData[1])
					c.send("Operation Success".encode())
				else:
					c.send("Operation Fail - check key or value or identation".encode())
			elif messageDecoded == "2":
				c.send(str(database).encode())
			else:
				c.send("Operation does not Exists".encode())
		c.close()
	except:
		print("An internal error occoured and "+str(addr)+" got disconected")


def start():
	s.listen(5)                                 # Now wait for client connections.
	print("[LISTENING] Server is listening on "+str(port))
	while True:
		c, addr = s.accept()                     # Establish connection with client.
		thread = threading.Thread(target=handle_client,args=(c,addr))
		thread.start()
		print("[ACTIVE CONNECTIONS] "+str((threading.activeCount()-1)))
	s.close()


print("[STARTING] server is starting...")
start()