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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)
  
  while True:
    op = menu()

    if op == 1 or op == 2:
      userid = int(input("Digite o id: "))
      username = input("Digite o dado: ")

      if op == 1:
        response = stub.insertNewClient(helloworld_pb2.InsertRequest(id=userid,name=username))
        print("Greeter client received: " + response.message)
      else:
        response = stub.updateClient(helloworld_pb2.ModifyRequest(id=userid,name=username))
        print("Greeter client received: " + response.message)
    elif op == 3 or op == 4:
      userid = int(input("Digite o id: "))

      if op == 3:
        response = stub.findClient(helloworld_pb2.FindRequest(id=userid))
        print("Greeter client received: " + response.message)
      else:
        response = stub.deleteClient(helloworld_pb2.DeleteRequest(id=userid))
        print("Greeter client received: " + response.message)
    else:
      print("Desconectando Administrador...")
      break


def menu():
  print("1 - Inserir novo Cliente")
  print("2 - Modificar um Cliente")
  print("3 - Procurar Cliente")
  print("4 - Apagar Cliente")
  print("5 - Sair")
  op = int(input("Escolha a operação desejada:"))
  return op

if __name__ == '__main__':
    logging.basicConfig()
    run()
