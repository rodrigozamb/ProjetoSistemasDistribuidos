# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

#Removendo comunicação por mqttp

#import paho.mqtt.client as mqtt
#broker = "localhost"
#client = mqtt.Client("admin")
#print("connecting to broker")
#client.connect(broker)

from concurrent import futures
import logging
import grpc
import socket
import struct
import helloworld_pb2
import helloworld_pb2_grpc
import time
import threading

####################################

db = dict([])

#Enviando atualização do banco para o processo responsável pelo ratis
#Informações enviadas para em (127.0.0.1, 5100)
def ratisSend(data):
  
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.connect(("localhost", 5100))
    s_socket.send(data.encode())
    s_socket.close()

#Recebendo atualização do banco do processo responsável pelo Ratis, requisitado pelos outros portais
#Informações recebidas em (224.1.1.1, 5101)
def ratisReceive():
  
  while True:
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", 5101))

    req = struct.pack("=4sl", socket.inet_aton("224.1.1.1"), socket.INADDR_ANY)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, req)
    data = s.recvfrom(1024)
    updateData(data)

#Atualização do banco de dados
def updateData(data):
   
   global db

   msg = []
   msg = str(data).split(",")
   
   #Extraindo informações
   msg[0] = msg[0].split("'")[1]
   msg[1] = int(msg[1].split("'")[0])
   msg[2] = msg[2].split("'")[0]
   
   if msg[0] == "add_client":
    if msg[1] not in db.keys():
      db[msg[1]] = msg[2]
   elif msg[0] == "update_client":
    db[msg[1]] = msg[2]
   elif msg[0] == "delete_client":
    del db[msg[1]]
      
   print(db)

class Greeter(helloworld_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

  def SayHelloAgain(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello again, %s!' % request.name)

  def insertNewClient(self, request, context):
    if request.id in db.keys():
      return helloworld_pb2.HelloReply(message='Error! Already exists a client with ID = %s' % request.id)
    print("Inserting new Client "+request.name+" with ID = "+str(request.id))
    
    #db[request.id] = request.name
    #print(db)
    #client.loop_start()
    #print("\nPublishing message to topic","/data") 
    #client.publish("/data", payload="I,"+str(request.id)+","+str(db[request.id]))
    #client.loop_stop()

    ratisSend("add_client,"+str(request.id)+","+str(request.name) + ",/n")
    
    return helloworld_pb2.HelloReply(message='Successfully created client with CID = %s!' % request.id)
  
  def updateClient(self,request,context):
    if request.id not in db.keys():
      return helloworld_pb2.HelloReply(message='Error! Client with CID = %s not found.' % request.id)
    
    #db[request.id] = request.name
    #print(db)
    #client.loop_start()
    #print("\nPublishing message to topic","/data") 
    #client.publish("/data", payload="U,"+str(request.id)+","+str(db[request.id]))
    #client.loop_stop()
    
    ratisSend("update_client,"+str(request.id)+","+str(request.name) + ",/n")
    
    return helloworld_pb2.HelloReply(message='Successfully updated client with CID = %s!' % request.id)

  def findClient(self, request, context):
    if request.id not in db.keys():
      return helloworld_pb2.HelloReply(message='Error! Client with CID = %s not found.' % request.id)
    
    return helloworld_pb2.HelloReply(message=db[request.id])

  def deleteClient(self, request, context):
    if request.id not in db.keys():
      return helloworld_pb2.HelloReply(message='Error! Client with CID = %s not found.' % request.id)
    
    #del db[request.id]
    #client.loop_start()
    #print("\nPublishing message to topic","/data") 
    #client.publish("/data", payload="D,"+str(request.id))
    #client.loop_stop()
    
    ratisSend("delete_client,"+str(request.id)+",/n")

    return helloworld_pb2.HelloReply(message='Successfully deleted client with CID = %s!' % request.id)

def serve():
  
    #Thread para comunicação com ratis
    threadsub = threading.Thread(target=ratisReceive, args=())
    threadsub.start()
   
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
