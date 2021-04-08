
#client.py

#!/usr/bin/python                      # This is client.py file

import socket                          # Import socket module


packageSize = 1024                     # Size of package to send or receive

s = socket.socket()                    # Create a socket object
host = socket.gethostname()            # Get local machine name
port = 12345                           # Reserve a port for your service.

s.connect((host, port))

def menu():

	print("1 - Inserir nova Tarefa")
	print("2 - Modificar uma Tarefa")
	print("3 - Listar tarefas")
	print("4 - Apagar todas tarefa")
	print("5 - Apagar uma tarefa")
	print("6 - Sair")
	op = input("Escolha a operação desejada:")
	return op


def run():
	flag = True

	while flag:

		msg = menu()
		
		# msg = input("Digite mensagem: ")
		s.send(msg.encode())

		if msg == "6":
			# s.send("SAIR".encode())
			break
		# é preciso que o usuario informe seu id? ou o portalCLiente ira perguntar ao portalAdmin??
		if msg == "1":
			print("Digite o seu ID, título e descrição da tarefa separados por vírgula ( ex: '1,Projeto SD, Fazer parte 1' ) ")
			insertData = input()
			s.send(insertData.encode())
		elif msg == "2":
			print("Digite o ID, título e a nova descrição da tarefa separados por vírgula ( ex: '1,Projeto SD, aprimorar parte 1' ) ")
			insertData = input()
			s.send(insertData.encode())
		elif msg == "3":
			print("Digite seu id:")
			userid = input()
			s.send(userid.encode())
		elif msg == "4":
			print("Digite seu id:")
			userid = input()
			s.send(userid.encode())
		elif msg == "5":
			print("Digite o ID e título da tarefa que deseja excluir separados por vírgula ( ex: '1,Projeto SD' ) ")
			insertData = input()
			s.send(insertData.encode())


			
		data = s.recv(1024)
		print("Mensagem recebida: ",data.decode())


	print("Desconectando Client...")
	s.close()

run()