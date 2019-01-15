'''
Created on 19-Apr-2018

@author: nisha
'''
from partition import Partition
from . import Operation
import os
import subprocess
import pickle
class Delete(object):
    
    def executeOperation(self,conn,commandClient, commandServer):
            partition = Partition()
            userFileName = commandServer.processDownload()
            hexValue = partition.findHash(userFileName)
            print(str(hexValue))
            remainder = partition.findShiftedValue(hexValue, userFileName, partition)
            disk1 = Partition.hashDiskMap[remainder]
            disk2 = Partition.hashDiskBackupMap[remainder]
            print("disk1:"+str(disk1)+" disk2:"+str(disk2))
            ipMachine = Partition.diskIpMap[disk1]
            print("IpMachine: "+ipMachine)
            print("Backup Disk: "+str(disk2))
            backupMachine = Partition.diskIpMap[disk2]
            print("Backup Machine: "+backupMachine)
            ipMachine = ipMachine + " " + backupMachine
            conn.send(ipMachine.encode('ascii')) 
            data1 = conn.recv(2048)
            msg = str(data1.decode('ascii'))
            print(str(msg))
            data1 = conn.recv(2048)
            msg = str(data1.decode('ascii'))
            print(str(msg))
            if os.path.getsize('hashFileMap.txt') == 0:
                hashFileMap={}
            else:
                with open('hashFileMap.txt', 'rb') as f:
                    hashFileMap = pickle.load(f)

            Partition.hashFileMap = hashFileMap
            isEmptyList = False
            hashValue = 0
            for hashV, fileN in Partition.hashFileMap.items():
                print(str(fileN))
                if userFileName in fileN:
                    fileN.remove(userFileName)
                    if not fileN:
                        isEmptyList = True
                        hashValue = hashV
            if isEmptyList == True:
                del Partition.hashFileMap[hashValue]
            print(userFileName)
            for hashV, fileN in Partition.hashFileMap.items():
                print(str(fileN))
            with open('hashFileMap.txt', 'wb') as handle:
                pickle.dump(Partition.hashFileMap, handle)


