import socket 
import sys
import traceback
import pickle
from threading import Thread 
from command import Command
from partition import Partition
from operation.factory import OperationFactory

class ClientThread(Thread): 

    def __init__(self, conn, ip, port):
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port
        self.conn = conn
        print("New server socket thread started for " + ip + ":" + str(port))
 
    def run(self): 
        while True :
            try: 
                message = self.conn.recv(8192) 
                if not message:
                    print("closed")
                    try:
                        self.conn.close()
                    except:
                        pass
                    return
                try:
                    #dataInfo = message.decode('ascii')
                    dataInfo = pickle.loads(message)
                    messageInfo = str(dataInfo)
                    print("recv:::::"+str(dataInfo)+"::")
                except UnicodeDecodeError:
                    print("non-ascii data")
                    continue
                except pickle.UnpicklingError as e:
                    # normal, somewhat expected
                    print(traceback.format_exc())
                    dataInfo = message.decode('ascii')
                    print("recvfromexc:::::"+str(dataInfo)+"::")
                    continue
                if dataInfo != '':
                    print( "Server received command:", messageInfo)
                    commandServer = Command(messageInfo)
                    command = commandServer.processCommand()
                    factory = OperationFactory()
                    factory.createOperation(command).executeOperation(self.conn, messageInfo,commandServer)  
            except socket.error:
                print("Unexpected error:", sys.exc_info()[0])
                try:
                    self.conn.close()
                except:
                    pass
                return
            except Exception as e:
                print(e.args)
                continue

serverCommand = input("Enter Server Command: ")
commandServer = Command(serverCommand)
command = commandServer.processCommand()
print(command)
if command == "server":
    partition,ipList  = commandServer.processServerCommand()
    partition = Partition(partition,ipList);
    partition.updateDiskHashTable();
    partition.updateDiskHashTable1();
    partition.updateDiskHashBackupTable1();
hostname = socket.gethostname()   
TCP_IP = socket.gethostbyname(hostname)
print("Server IP Address: "+TCP_IP)
print("Server Host Name: "+hostname)
BUFFER_SIZE = 1024  
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, 0))  
tcpServer.listen(10)
port = str(tcpServer.getsockname()[1])
print("Port:"+ port)
print("client "+TCP_IP+" "+port)
threads = [] 
 
while True: 
    print( "Waiting for connections from clients..." )
    (conn, (ip,port)) = tcpServer.accept()   
    newthread = ClientThread(conn,ip,port)
    newthread.daemon = True 
    newthread.start() 




