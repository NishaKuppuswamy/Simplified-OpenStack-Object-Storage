# Import socket module
import socket
import sys
from CommandClient import CommandClient
from operation.factory import OperationFactory
import logging
import pickle
import traceback

def Main():
    clientCommand = input("Enter Command")
    commandClient = CommandClient(clientCommand)
    command,user= commandClient.processClient()
    print(command)
    if command == "client":
        host, port = commandClient.processClientCommand()
    
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip = commandClient.processHost(host)
    s.connect((ip,int(port)))

    while True:
        try:
            message = input("Enter Command: ")
            commandClient = CommandClient(message)
            command, user = commandClient.processCommand()
            if command == "error":
                print("Invalid Command. Enter Again.")   
            else: 
                factory = OperationFactory()
                obj = factory.createOperation(command)
                if obj == "error":
                   print("Invalid Command. Enter Again.")
                else:
                   data = pickle.dumps(message)
                   s.send(data)
                   obj.executeOperation(s, commandClient)
        except ValueError as e:
            print(e.args)
            data = pickle.dumps(str(e))
            s.send(data)
            continue
        except OSError as e:
            logging.error(str(e))
            data = pickle.dumps(str(e))
            s.send(data)
            continue
        except Exception as e:
            print(e.args)
            data = pickle.dumps(str(e))
            s.send(data)
            continue
            

if __name__ == '__main__':
        Main()
