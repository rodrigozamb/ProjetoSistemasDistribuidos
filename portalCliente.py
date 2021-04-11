# server.py
#!/usr/bin/python                           # This is server.py file

import socket                               # Import socket module
import threading

####################################
import paho.mqtt.client as mqtt
import time

database = dict([])
users = dict([])

def on_message(client, userdata, message):
   global users

   print("\n",str(message.payload.decode("utf-8")))
   msg = []
   msg = str(message.payload.decode("utf-8")).strip().split(",")

   if msg[0] == "I":
      if msg[0] not in users.keys():
         users[msg[1]] = msg[2]
   elif msg[0] == "U":
      users[msg[1]] = msg[2]
   elif msg[0] == "D":
      del users[msg[1]]
      
   print(users)
   if message.retain == 1:
      print("This is a retained message")


broker = "localhost"
client = mqtt.Client("client")
print("connecting to broker")
client.connect(broker)
####################################

packageSize = 1024

s = socket.socket()                         # Create a socket object
# host = socket.gethostname()                 # Get local machine name
host = "localhost"                 # Get local machine name
port = 12345                                # Reserve a port for your service.
s.bind((host, port))                        # Bind to the port


def subscribeToTopic():
   global client
   client.subscribe("/data", 0)
   client.on_message = on_message
   while True: 
      client.loop()

def handle_client(c, addr):
   global database
   print('Got connection from', addr)
   flag = True

   try:
      while flag:
         data = c.recv(1024)
         messageDecoded = data.decode()
         print("["+str(addr)+"] Mensagem recebida: "+messageDecoded)
         if messageDecoded == "6":
               print("desconectando cliente")
               flag = False
               break

         if messageDecoded == "1":

               # adicionar uma nova tarefa
               idata = c.recv(1024)
               insertData = idata.decode()
               insertData = insertData.split(",")

               if len(insertData) == 3:
                  if insertData[0] not in users.keys():
                     c.send(
                     "Operation Fail - invalid CID".encode())
                  else:
                     if insertData[0] not in database.keys():
                        database[insertData[0]] = []

                     database[insertData[0]].append(
                        (insertData[1], insertData[2]))
                     print(database)
                     c.send("Operation Success".encode())
               else:
                  c.send(
                     "Operation Fail - check key or value or identation".encode())

         elif messageDecoded == "2":
               # alterar uma tarefa
               idata = c.recv(1024)
               insertData = idata.decode()
               insertData = insertData.split(",")

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

         elif messageDecoded == "3":
               # listar tarefas
               idata = c.recv(1024)
               insertData = idata.decode()

               userid = insertData
               exists = False

               if len(userid) == 1:
                  if insertData[0] not in users.keys():
                     c.send(
                     "Operation Fail - invalid CID".encode())
                  else:
                     if userid not in users.keys():
                        c.send(
                        "Operation Fail - invalid CID".encode())
                     else:
                        if userid not in database.keys():
                           c.send("User does not have tasks".encode())
                        else:
                           resp = str(database[userid])
                           c.send(resp.encode())

               else:
                  c.send(
                     "Operation Fail - check key or value or identation".encode())

         elif messageDecoded == "4":
               # apagar todas tarefas
               idata = c.recv(1024)
               insertData = idata.decode()

               userid = insertData

               if len(userid) == 1:
                  if insertData[0] not in users.keys():
                     c.send(
                     "Operation Fail - invalid CID".encode())
                  else:
                     if userid not in database.keys():
                        c.send("Operation Fail - User does not have tasks".encode())
                     else:
                        database[userid] = []
                        c.send("Operation Success".encode())
               else:
                  c.send(
                     "Operation Fail - check key or value or identation".encode())

         elif messageDecoded == "5":
               # apagar uma tarefa
               idata = c.recv(1024)
               insertData = idata.decode()
               insertData = insertData.split(",")

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
   # Now wait for client connections.
   s.listen(5)
   print("[LISTENING] Server is listening on "+str(port))

   threadsub = threading.Thread(target=subscribeToTopic, args=())
   threadsub.start()
   
   while True:
      # Establish connection with client.
      c, addr = s.accept()
      thread = threading.Thread(target=handle_client, args=(c, addr))
      thread.start()
      print("[ACTIVE CONNECTIONS] "+str((threading.activeCount()-1)))
   s.close()


print("[STARTING] server is starting...")
start()
