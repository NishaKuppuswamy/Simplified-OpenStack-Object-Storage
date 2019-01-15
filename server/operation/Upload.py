'''
Created on 19-Apr-2018

@author: nisha
'''
from partition import Partition
from command import Command
import os
import pickle
#from . import Operation

class Upload(object):

    def executeOperation(self,conn,message, commandServer):
        userFileName = commandServer.processUploadForServer()
        partition = Partition()
        hexValue = partition.findHash(userFileName)
        print(str(hexValue))
        remainder = partition.findShiftedValue(hexValue, userFileName, partition)
        self.updateFileMap(userFileName, remainder)
        disk1 = Partition.hashDiskMap[remainder]
        disk2 = Partition.hashDiskBackupMap[remainder]
        print("disk1:"+str(disk1)+" disk2:"+str(disk2))
        ipMachine = Partition.ipList[disk1]
        print("IpMachine: "+ipMachine)
        print("Backup Disk: "+str(disk2))
        backupMachine = Partition.ipList[disk2]
        print("Backup Machine: "+backupMachine)
        ipMachine = ipMachine + " " + backupMachine
        conn.send(ipMachine.encode('ascii'))
        data = conn.recv(2048)
        msgs = str(data.decode('ascii'))
        if msgs != "no data":
            msgList = msgs.split("%")
            msgSize = len(msgList)
            i=0
            while i<msgSize:
              print(str(msgList[i]))
              i+=1

        
    def updateFileMap(self, userFileName, remainder):
        if os.path.getsize('hashFileMap.txt') == 0:
           hashFileMap={}
        else:
           with open('hashFileMap.txt', 'rb') as f:
               hashFileMap = pickle.load(f)
               
        Partition.hashFileMap = hashFileMap
        if remainder in Partition.hashFileMap:
             print("here")
             userFileList = Partition.hashFileMap.get(remainder)
             if userFileName not in userFileList:
                 userFileList.append(userFileName)
             Partition.hashFileMap[remainder] = userFileList
        else:
             print("or here")
             userFileList = []
             userFileList.append(userFileName)
             Partition.hashFileMap[remainder] = userFileList
        for k, v in Partition.hashFileMap.items():
            print(k, v)
        with open('hashFileMap.txt', 'wb') as handle:
            pickle.dump(Partition.hashFileMap, handle)

        if remainder in Partition.hashBackupFileMap:
             userFileList = Partition.hashBackupFileMap.get(remainder)
             userFileList.append(userFileName)
             Partition.hashBackupFileMap[remainder] = userFileList
        else:
            userFileList = []
            userFileList.append(userFileName)
            Partition.hashBackupFileMap[remainder] = userFileList
        for hashV,fileL in Partition.hashFileMap.items():
            print(str(hashV))
            for fileN in fileL:
                print(str(fileN))
 
