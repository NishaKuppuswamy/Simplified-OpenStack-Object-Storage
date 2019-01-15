'''
Created on 27-Apr-2018

@author: nisha
'''
from partition import Partition
import copy
from bo.FileMigrate import FileMigrate
import pickle
import os
import struct

class Add(object):
    
    def executeOperation(self,conn,commandClient, commandServer):
        ipAddress = commandServer.getIpfromCommand()
        if ipAddress not in Partition.ipList:
            conn.send("Not Found".encode('ascii'))
            oldHashDisk = copy.deepcopy(Partition.hashDiskMap)
            oldBackupHashDisk = copy.deepcopy(Partition.hashDiskBackupMap)
            if os.path.getsize('hashFileMap.txt') == 0:
               hashFileMap={}
            else:
               with open('hashFileMap.txt', 'rb') as f:
                   hashFileMap = pickle.load(f)
            Partition.hashFileMap = hashFileMap
            changedHashList = self.addDisktoMap()
            moveHashList = list(set(changedHashList) & set(Partition.hashFileMap.keys()))
            changedBackupHashList =  self.addDisktoBackupMap()
            moveBackupHashList = list(set(changedBackupHashList) & set(Partition.hashFileMap.keys()))
            disk = self.findNextDisk()
            print("disk: "+str(disk)+ipAddress)
            Partition.diskIpMap[disk] = ipAddress
            Partition.ipList.append(ipAddress)
            
            for k, v in Partition.hashFileMap.items():
                print(k, v)
                disk = Partition.hashDiskMap[k]
                print(Partition.ipList[disk])
            migrateList = []
            for hashVal in moveHashList:
                print("Main Table Partition Details: ")
                newDisk = Partition.hashDiskMap[hashVal]
                oldDisk = oldHashDisk[hashVal]
                #print("newDisk:"+str(newDisk)+" oldDisk:"+str(oldDisk))
                fileList = Partition.hashFileMap[hashVal]
                newIpAdd = Partition.ipList[newDisk]
                oldIpAdd = Partition.ipList[oldDisk]
                print("Partition: "+str(hashVal)+" newIpAdd: "+str(newIpAdd) +" oldIp: "+str(oldIpAdd)+" FileNames: "+str(fileList))
                fileMigrate = FileMigrate(oldIpAdd, newIpAdd, fileList, hashVal)
                migrateList.append(fileMigrate)
            migrationData = pickle.dumps(migrateList)
            msg = struct.pack('>I', len(migrationData)) + migrationData
            conn.sendall(msg)
            migrateBackupList = []
            for hashVal in moveBackupHashList:
                print("Backup Table Partition Details: ")
                newDisk = Partition.hashDiskBackupMap[hashVal]
                oldDisk = oldBackupHashDisk[hashVal]
                #print("Backup newDisk:"+str(newDisk)+" Backup oldDisk:"+str(oldDisk))
                fileList = Partition.hashFileMap[hashVal]
                newIpAdd = Partition.ipList[newDisk]
                oldIpAdd = Partition.ipList[oldDisk]
                print("Partition: "+str(hashVal)+" newIpAdd: "+str(newIpAdd) +" oldIp: "+str(oldIpAdd)+" FileNames: "+str(fileList))
                fileMigrate = FileMigrate(oldIpAdd, newIpAdd, fileList, hashVal)
                migrateBackupList.append(fileMigrate)
            
            migrationBackupData = pickle.dumps(migrateBackupList)
            msg = struct.pack('>I', len(migrationBackupData)) + migrationBackupData
            conn.sendall(msg)
            #print("sentt")
        else:
            conn.send("Found".encode('ascii'))
            
    def addDisktoMap(self):
        size = len(Partition.ipList)
        slots = int(Partition.rangeVal/(size+1))
        disk = self.findNextDisk()
        print(str(disk))
        i=0
        while i<size:
            x = list({k for k, v in Partition.hashDiskMap.items() if v ==i})
            if x:
                x = x[::-1]
                slotIndex = x[0]
                slotCount = 1
                while slotCount <=slots:
                    Partition.hashDiskMap[slotIndex] = disk
                    slotCount = slotCount+1
                    slotIndex = slotIndex-1
            i=i+1
        return list({k for k, v in Partition.hashDiskMap.items() if v == disk}) 
        
    
    def addDisktoBackupMap(self):
        size = len(Partition.ipList)
        slots = int(Partition.rangeVal/(size+1))
        disk = self.findNextDisk()
        print(str(disk))
        i=0
        while i<size:
            x = list({k for k, v in Partition.hashDiskBackupMap.items() if v ==i})
            x = x[::-1]
            slotIndex = x[0]
            slotCount = 1
            while slotCount <=slots:
                Partition.hashDiskBackupMap[slotIndex] = disk
                slotCount = slotCount+1
                slotIndex = slotIndex-1
            i=i+1
        return list({k for k, v in Partition.hashDiskBackupMap.items() if v == disk})
  
    def findNextDisk(self):
        maxVal = 0
        for disk,ip in Partition.diskIpMap.items():
            if disk > maxVal:
                maxVal = disk
        return maxVal+1
