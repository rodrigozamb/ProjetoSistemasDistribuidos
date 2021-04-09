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

from concurrent import futures
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

####################################
import paho.mqtt.client as mqtt
import time

broker = "localhost"

print("creating new instance")

client = mqtt.Client("admin")

print("connecting to broker")
client.connect(broker)
####################################

db = dict([])

class Greeter(helloworld_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

  def SayHelloAgain(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello again, %s!' % request.name)

  def insertNewClient(self, request, context):
    if request.id in db.keys():
      return helloworld_pb2.HelloReply(message='Error! Already exists a client with ID = %s' % request.id)
    print("Inserting new Client "+request.name+" with ID = "+str(request.id))
    db[request.id] = request.name
    print(db)

    client.loop_start()
    print("Publishing message to topic","/data") 
    client.publish("/data", payload="I,"+str(request.id)+","+str(db[request.id]))
    client.loop_stop()

    return helloworld_pb2.HelloReply(message='Successfully created client with CID = %s!' % request.id)
  
  def updateClient(self,request,context):
    if request.id not in db.keys():
      return helloworld_pb2.HelloReply(message='Error! Client with CID = %s not found.' % request.id)
    db[request.id] = request.name
    print(db)

    client.loop_start()
    print("Publishing message to topic","/data") 
    client.publish("/data", payload="U,"+str(request.id)+","+str(db[request.id]))
    client.loop_stop()

    return helloworld_pb2.HelloReply(message='Successfully updated client with CID = %s!' % request.id)

  def findClient(self, request, context):
    if request.id not in db.keys():
      return helloworld_pb2.HelloReply(message='Error! Client with CID = %s not found.' % request.id)
    
    return helloworld_pb2.HelloReply(message=db[request.id])

  def deleteClient(self, request, context):
    if request.id not in db.keys():
      return helloworld_pb2.HelloReply(message='Error! Client with CID = %s not found.' % request.id)
    del db[request.id]

    client.loop_start()
    print("Publishing message to topic","/data") 
    client.publish("/data", payload="D,"+str(request.id))
    client.loop_stop()

    return helloworld_pb2.HelloReply(message='Successfully deleted client with CID = %s!' % request.id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()




if __name__ == '__main__':
    logging.basicConfig()
    serve()
