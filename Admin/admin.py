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
from adminMenuEnum import adminMenuEnum

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

def validateUserIDType():
  while True:
    userid = input("Digite o id: ")

    if not userid.isdigit():
      print('**ID must be an integer**')
    else:
      break
  return int(userid)

def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)
  
  while True:
    op = menu()

    if op == adminMenuEnum.INSERIR_CLIENTE.value or op == adminMenuEnum.MODIFICAR_CLIENTE.value:
      userid = validateUserIDType()
      username = input("Digite o nome de usuario: ")

      if op == adminMenuEnum.INSERIR_CLIENTE.value:
        response = stub.insertNewClient(helloworld_pb2.InsertRequest(id=userid,name=username))
        print("\nGreeter client received: " + response.message)
      else:
        response = stub.updateClient(helloworld_pb2.ModifyRequest(id=userid,name=username))
        print("\nGreeter client received: " + response.message)
    elif op == adminMenuEnum.PROCURAR_CLIENTE.value or op == adminMenuEnum.APAGAR_CLIENTE.value:
      userid = validateUserIDType()

      if op == adminMenuEnum.PROCURAR_CLIENTE.value:
        response = stub.findClient(helloworld_pb2.FindRequest(id=userid))
        print("Greeter client received: " + response.message)
      else:
        response = stub.deleteClient(helloworld_pb2.DeleteRequest(id=userid))
        print("Greeter client received: " + response.message)
    else:
      print("Desconectando Administrador...")
      break


def menu():
  print("\n-------------MENU-------------")
  print(f"{adminMenuEnum.INSERIR_CLIENTE.value} - Inserir novo Cliente")
  print(f"{adminMenuEnum.MODIFICAR_CLIENTE.value} - Modificar um Cliente")
  print(f"{adminMenuEnum.PROCURAR_CLIENTE.value} - Procurar Cliente")
  print(f"{adminMenuEnum.APAGAR_CLIENTE.value} - Apagar Cliente")
  print(f"{adminMenuEnum.SAIR.value} - Sair")
  op = int(input("Escolha a operação desejada:"))
  return op

if __name__ == '__main__':
    logging.basicConfig()
    run()
