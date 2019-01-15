'''
Created on 19-Apr-2018

@author: nisha
'''
from partition import Partition
from . import Operation
import pickle
import os
from bo.FileMigrate import FileMigrate
class List(object):
    
    def executeOperation(self,conn,commandClient,commandServer):
           userName = commandServer.getUserNamefromCommand()
           i=0
           ipListString = ""
           ipListSize = len(Partition.ipList)
           while i<ipListSize-1:
              print("ip: "+str(Partition.ipList[i]))
              ipListString = ipListString + Partition.ipList[i]+" "
              i+=1
           ipListString = ipListString + Partition.ipList[i]
           print("ip"+ipListString)
           conn.send(ipListString.encode('ascii'))  
           if os.path.getsize('hashFileMap.txt') == 0:
               hashFileMap={}
           else:
               with open('hashFileMap.txt', 'rb') as f:
                   hashFileMap = pickle.load(f)
           Partition.hashFileMap = hashFileMap
           migrateList = []
           for hashVal, fileList in Partition.hashFileMap.items():
              for fileName in fileList:
                  fileSplit = fileName.split("/")
                  if fileSplit[1] and fileSplit[0] == userName:
                      mainDisk = Partition.hashDiskMap[hashVal]
                      #print(str(mainDisk))
                      backupDisk = Partition.hashDiskBackupMap[hashVal] 
                      #print(str(backupDisk))
                      mainIp =  Partition.diskIpMap[mainDisk]
                      backupIp =  Partition.diskIpMap[backupDisk]
                      fileMigrate = FileMigrate()
                      fileMigrate.updateIpDetails(mainIp, backupIp,fileSplit[1])
                      migrateList.append(fileMigrate)
           migrationData = pickle.dumps(migrateList)
           conn.send(migrationData)
           data = conn.recv(2048)
           msgs = str(data.decode('ascii'))
           msgList = msgs.split("%")
           msgSize = len(msgList)
           i=0
           while i<msgSize:
               print(str(msgList[i]))
               i+=1
 
