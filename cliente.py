#client.py
#!/usr/bin/python         

import socket               
from config import *
from clienteMenuEnum import clienteMenuEnum

s = socket.socket()                  
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Host e porta agora vem do arquivo de configuração "config.py" #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# host = "localhost"           
# port = 12345                        

def connect_client(host,port):
	print("attemp to connect to Client with port - ",port)
	try:
		s.connect((host, port))                        # Bind to the port
	except:
		return connect_client(host,port+1)
	return host,port

connect_client(host, port)
# s.connect((host, port))

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
	print(f"{clienteMenuEnum.INSERIR_TAREFA.value} - Inserir nova Tarefa")
	print(f"{clienteMenuEnum.MODIFICAR_TAREFA.value} - Modificar uma Tarefa")
	print(f"{clienteMenuEnum.LISTAR_TAREFA.value} - Listar tarefas")
	print(f"{clienteMenuEnum.APAGAR_TODAS_TAREFAS.value} - Apagar todas tarefa")
	print(f"{clienteMenuEnum.APAGAR_UMA_TAREFA.value} - Apagar uma tarefa")
	print(f"{clienteMenuEnum.SAIR.value} - Sair")
	op = input("Escolha a operação desejada:")
	return op


def run():
	flag = True

	while flag:

		msg = menu()
		s.send(msg.encode())

		if int(msg) == clienteMenuEnum.SAIR.value:
			# s.send("SAIR".encode())
			break
		if int(msg) == clienteMenuEnum.INSERIR_TAREFA.value:
			print("\nDigite o seu ID, título e descrição da tarefa separados por vírgula ( ex: '1,Projeto SD, Fazer parte 1' ) ")
			insertData = input()
			s.send(insertData.encode())
		elif int(msg) == clienteMenuEnum.MODIFICAR_TAREFA.value:
			print("\nDigite o ID, título e a nova descrição da tarefa separados por vírgula ( ex: '1,Projeto SD, aprimorar parte 1' ) ")
			insertData = input()
			s.send(insertData.encode())
		elif int(msg) == clienteMenuEnum.LISTAR_TAREFA.value:
			print("\nDigite seu id:")
			userid = input()
			s.send(userid.encode())
		elif int(msg) == clienteMenuEnum.APAGAR_TODAS_TAREFAS.value:
			print("\nDigite seu id:")
			userid = input()
			s.send(userid.encode())
		elif int(msg) == clienteMenuEnum.APAGAR_UMA_TAREFA.value:
			print("\nDigite o ID e título da tarefa que deseja excluir separados por vírgula ( ex: '1,Projeto SD' ) ")
			insertData = input()
			s.send(insertData.encode())
			
		data = s.recv(packageSize)
		print("\nMensagem recebida: ",data.decode())

	print("Desconectando Cliente...")
	s.close()

run()