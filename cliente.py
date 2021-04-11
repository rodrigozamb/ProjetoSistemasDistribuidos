#client.py
#!/usr/bin/python         

import socket               

packageSize = 1024                  

s = socket.socket()                  
host = "localhost"           
port = 12345                        

s.connect((host, port))

def validateUserIDType():
  while True:
    userid = input("Digite o id: ")

    if not userid.isdigit():
      print('**ID must be an integer**')
    else:
      break
  return int(userid)

def menu():

	print("\n-------------MENU-------------")
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
		s.send(msg.encode())

		if msg == "6":
			# s.send("SAIR".encode())
			break
		if msg == "1":
			print("\nDigite o seu ID, título e descrição da tarefa separados por vírgula ( ex: '1,Projeto SD, Fazer parte 1' ) ")
			insertData = input()
			s.send(insertData.encode())
		elif msg == "2":
			print("\nDigite o ID, título e a nova descrição da tarefa separados por vírgula ( ex: '1,Projeto SD, aprimorar parte 1' ) ")
			insertData = input()
			s.send(insertData.encode())
		elif msg == "3":
			print("\nDigite seu id:")
			userid = input()
			s.send(userid.encode())
		elif msg == "4":
			print("\nDigite seu id:")
			userid = input()
			s.send(userid.encode())
		elif msg == "5":
			print("\nDigite o ID e título da tarefa que deseja excluir separados por vírgula ( ex: '1,Projeto SD' ) ")
			insertData = input()
			s.send(insertData.encode())
			
		data = s.recv(1024)
		print("\nMensagem recebida: ",data.decode())

	print("Desconectando Cliente...")
	s.close()

run()