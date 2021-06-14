#Removendo comunicação por mqttp

#import paho.mqtt.client as mqtt
#def on_message(client, userdata, message):
#   global users

#   print("\n",str(message.payload.decode("utf-8")))
#   msg = []
#   msg = str(message.payload.decode("utf-8")).strip().split(",")

#   if msg[0] == "I":
#      if msg[0] not in users.keys():
#         users[msg[1]] = msg[2]
#   elif msg[0] == "U":
#      users[msg[1]] = msg[2]
#   elif msg[0] == "D":
#      del users[msg[1]]
      
#   print(users)
#   if message.retain == 1:
#      print("This is a retained message")

#broker = "localhost"
#client = mqtt.Client("client")
#print("connecting to broker")
#client.connect(broker)

#def subscribeToTopic():
#   global client
#   client.subscribe("/data", 0)
#   client.on_message = on_message
#   while True: 
#      client.loop()

import socket  
import threading
import struct
from config import *
import time
from clienteMenuEnum import clienteMenuEnum 

database = dict([])
users = dict([])

def connect_portal(host,port):
   print("attemp to connect Portal with port - ",port)
   try:
      s.bind((host, port))                      
   except:
      return connect_portal(host,port+1)
   return host,port

####################################

s = socket.socket()
portal_host, portal_port = connect_portal(host,port)

#Atualização do banco de dados
def updateData(data):
   
   global users

   msg = []
   msg = str(data).split(",")
   
   #Extraindo informações
   msg[0] = msg[0].split("'")[1]
   msg[1] = int(msg[1].split("'")[0])
   msg[2] = msg[2].split("'")[0]
   
   if msg[0] == "add_client":
      if msg[1] not in users.keys():
         users[msg[1]] = msg[2]
   elif msg[0] == "update_client":
      users[msg[1]] = msg[2]
   elif msg[0] == "delete_client":
      del users[msg[1]]
      
   print(users)
   print(database)
   
#Recebendo atualização do banco do processo responsável pelo Ratis, requisitado pelos outros portais
#Informações recebidas em (224.1.1.1, 5101)
def ratisReceive():
  
  while True:
    
    r_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    r_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    r_socket.bind(("224.1.1.1", 5101))

    req = struct.pack("=4sl", socket.inet_aton("224.1.1.1"), socket.INADDR_ANY)
    r_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, req)
    data = r_socket.recvfrom(1024)
    updateData(data)

def handle_client(c, addr):
   global database
   print('Got connection from', addr)
   flag = True

   try:
      while flag:
         data = c.recv(packageSize)
         messageDecoded = data.decode()
         print("["+str(addr)+"] Mensagem recebida: "+messageDecoded)
         if int(messageDecoded) == clienteMenuEnum.SAIR.value:
               print("desconectando cliente")
               flag = False
               break

         if int(messageDecoded) == clienteMenuEnum.INSERIR_TAREFA.value:

               # adicionar uma nova tarefa
               idata = c.recv(packageSize)
               insertData = idata.decode()
               insertData = insertData.split(",")
               insertData[0] = int(insertData[0])

               if len(insertData) == 3:
                  if insertData[0] not in users.keys():
                     c.send(
                     "Operation Fail - invalid CID".encode())
                  else:
                     if insertData[0] not in database.keys():
                        database[insertData[0]] = []

                     database[insertData[0]].append((insertData[1], insertData[2]))
                     
                     print(database)
                     c.send("Operation Success".encode())
               else:
                  c.send(
                     "Operation Fail - check key or value or identation".encode())

         elif int(messageDecoded) == clienteMenuEnum.MODIFICAR_TAREFA.value:
               # alterar uma tarefa
               idata = c.recv(packageSize)
               insertData = idata.decode()
               insertData = insertData.split(",")
               insertData[0] = int(insertData[0])

               if len(insertData) == 3:
                  if insertData[0] not in users.keys():
                     c.send(
                     "Operation Fail - invalid CID".encode())
                  else:
                     userid = insertData[0]

                  if userid not in database.keys():
                     c.send("Operation Fail - Task not found".encode())
                  else:
                     index = -1
                     for i in range(0, len(database[userid])):
                           if(database[userid][i][0] == insertData[1]):
                              index = i
                              break

                     if index == -1:
                           c.send("Operation Fail - Task not found".encode())
                     else:
                           database[userid][index] = (
                              insertData[1], insertData[2])
                           c.send("Operation Success".encode())
               else:
                  c.send(
                     "Operation Fail - check key or value or identation".encode())

         elif int(messageDecoded) == clienteMenuEnum.LISTAR_TAREFA.value:
               # listar tarefas
               idata = c.recv(packageSize)
               insertData = idata.decode()
               insertData = insertData.split(",")
               insertData[0] = int(insertData[0])

               exists = False

               if len(insertData) == 1:
                  if insertData[0] not in users.keys():
                     c.send(
                     "Operation Fail - invalid CID".encode())
                  else:
                     if insertData[0] not in users.keys():
                        c.send(
                        "Operation Fail - invalid CID".encode())
                     else:
                        if insertData[0] not in database.keys():
                           c.send("User does not have tasks".encode())
                        else:
                           resp = str(database[insertData[0]])
                           c.send(resp.encode())

               else:
                  c.send(
                     "Operation Fail - check key or value or identation".encode())

         elif int(messageDecoded) == clienteMenuEnum.APAGAR_TODAS_TAREFAS.value:
               # apagar todas tarefas
               idata = c.recv(packageSize)
               insertData = idata.decode()
               insertData = insertData.split(",")
               insertData[0] = int(insertData[0])

               if len(insertData) == 1:
                  if insertData[0] not in users.keys():
                     c.send(
                     "Operation Fail - invalid CID".encode())
                  else:
                     if insertData[0] not in database.keys():
                        c.send("Operation Fail - User does not have tasks".encode())
                     else:
                        database[insertData[0]] = []
                        c.send("Operation Success".encode())
               else:
                  c.send(
                     "Operation Fail - check key or value or identation".encode())

         elif int(messageDecoded) == clienteMenuEnum.APAGAR_UMA_TAREFA.value:
               # apagar uma tarefa
               idata = c.recv(packageSize)
               insertData = idata.decode()
               insertData = insertData.split(",")
               insertData[0] = int(insertData[0])

               if len(insertData) == 2:
                  if insertData[0] not in users.keys():
                     c.send(
                     "Operation Fail - invalid CID".encode())
                  else:
                     userid = insertData[0]

                  if userid not in database.keys():
                     c.send("Operation Fail - Task not found".encode())
                  else:
                     index = -1
                     for i in range(0, len(database[userid])):
                           if(database[userid][i][0] == insertData[1]):
                              index = i
                              break

                     if index == -1:
                           c.send("Operation Fail - Task not found".encode())
                     else:
                           del database[userid][index]
                           
                           c.send("Operation Success".encode())
               else:
                  c.send(
                     "Operation Fail - check key or value or identation".encode())
         else:
               c.send("Operation does not Exists".encode())
      c.close()
   except:
      print("An internal error occoured and "+str(addr)+" got disconected")

def start():
   
   #Thread para comunicação com ratis
   threadsub = threading.Thread(target=ratisReceive, args=())
   threadsub.start()
    
   # Now wait for client connections.
   s.listen(5)
   global portal_port
   print("[LISTENING] Server is listening on "+str(portal_port))
   
   while True:
      # Establish connection with client.
      c, addr = s.accept()
      thread = threading.Thread(target=handle_client, args=(c, addr))
      thread.start()
      print("[ACTIVE CONNECTIONS] "+str((threading.activeCount()-1)))
   s.close()

print("[STARTING] server is starting...")
start()
