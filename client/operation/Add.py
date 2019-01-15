'''
Created on 29-Apr-2018

@author: nisha
'''
'''
Created on 19-Apr-2018

@author: nisha
'''
import os
import logging
import pickle
import struct
#from . import Operation

class Add(object):
    
    def executeOperation(self,s,commandClient):
            command,ip= commandClient.processClient()
            isValid = commandClient.processIpAddress()
            if isValid == "error":
                raise ValueError("Invalid IP Address. Enter Again.")
           # s.send(ip.encode('ascii'))
            #data = s.recv(32768)
            #migrationList = pickle.loads(data)
            data1 = s.recv(1024)
            isFound = str(data1.decode('ascii'))
            if isFound == "Not Found":
                migrationList = []
                raw_msglen = self.recvall(s, 4)
                if raw_msglen:
                    msglen = struct.unpack('>I', raw_msglen)[0]
            # Read the message data
                    data =  self.recvall(s, msglen)
                    if data:
                        migrationList = pickle.loads(data)
    
                try:
                    for migrationObj in migrationList:
                        print("Main Table Partition Details:")
                        oldIp = migrationObj.oldIp
                        newIp = migrationObj.newIp
                        partition = migrationObj.hashVal
                        print("Partition: "+str(partition)+"oldip: "+oldIp+"newIp: "+newIp)
                        fileList = migrationObj.fileList
                        for file in fileList:
                            print("FileName"+file)
                            fileSplit = file.split("/")
                            sshCommand = "ssh " +os.getlogin()+"@"+newIp+" \"mkdir -p "+ "/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/\""
                            scpCommand = "scp -B "+os.getlogin()+"@"+oldIp+":/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"+fileSplit[1]+ " "+os.getlogin()+"@"+newIp+":/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"+fileSplit[1]
                            sshCommand1 = "ssh " +os.getlogin()+"@"+oldIp+" rm "+ "/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"+fileSplit[1]
                            os.system(sshCommand)
                            os.system(scpCommand)
                            os.system(sshCommand1)
                           # print(str(sshCommand))
                           # print(str(scpCommand))
                           # print(str(sshCommand1))
                    migrationBackupList = []    
                    raw_msglen1 = self.recvall(s, 4)
                    if raw_msglen1:
                        msglen1 = struct.unpack('>I', raw_msglen1)[0]
                        data1 =  self.recvall(s, msglen1)
                        if data1:
                            migrationBackupList = pickle.loads(data1)
                #data = s.recv(8192)
                #migrationBackupList = pickle.loads(data)
                               
     
                    for migrationObj in migrationBackupList:
                        print("Backup Table Partition Details:")
                        oldIp = migrationObj.oldIp
                        newIp = migrationObj.newIp
                        partition = migrationObj.hashVal
                        print("Partition: "+str(partition)+"oldip: "+oldIp+"newIp: "+newIp)
                        fileList = migrationObj.fileList
                        for file in fileList:
                            print("FileName"+file)
                            fileSplit = file.split("/")
                            sshCommand = "ssh " +os.getlogin()+"@"+newIp+" \"mkdir -p "+ "/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/\""
                            scpCommand = "scp -B "+os.getlogin()+"@"+ip+":/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"+fileSplit[1]+ " "+os.getlogin()+"@"+newIp+":/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"+fileSplit[1]
                            sshCommand1 = "ssh " +os.getlogin()+"@"+ip+" rm "+ "/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"+fileSplit[1]
                            os.system(sshCommand)
                            os.system(scpCommand)
                            os.system(sshCommand1)
                            #print(str(sshCommand))
                            #print(str(scpCommand))
                            #print(str(sshCommand1))  
    
                except OSError as e:
                    logging.error(str(e))
            else:
                raise ValueError("IP Address already exists. Enter a non existing IP")            
    def recvall(self, sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
       data = b''
       while len(data) < n:
          packet = sock.recv(n - len(data))
          if not packet:
            return None
          data += packet
       return data
