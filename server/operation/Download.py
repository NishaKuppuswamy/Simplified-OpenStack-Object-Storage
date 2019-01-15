'''
Created on 19-Apr-2018

@author: nisha
'''
from . import Operation
import os
from partition import Partition
from command import Command

class Download(object):
    
    def executeOperation(self,conn,commandClient, commandServer):
        partition = Partition()
        userFileName = commandServer.processDownload()
        hexValue = partition.findHash(userFileName)
        print(str(hexValue))
        remainder = partition.findShiftedValue(hexValue, userFileName, partition)
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
        msg = str(data.decode('ascii'))
        print(str(msg))
       
