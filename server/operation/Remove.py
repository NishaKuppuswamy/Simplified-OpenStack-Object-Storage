'''
Created on 29-Apr-2018

@author: nisha
'''
'''
Created on 19-Apr-2018

@author: nisha
'''

import pickle
from bo.FileMigrate import FileMigrate
from partition import Partition
import copy
import os
import struct

class Remove(object):
    
    def executeOperation(self,conn,commandClient, commandServer):
        ipAddress = commandServer.getIpfromCommand()
        if ipAddress in Partition.ipList:
            conn.send("Found".encode('ascii'))
            diskToDel = self.findDiskForIp(ipAddress)
            print("disktodel"+str(diskToDel))
            if os.path.getsize('hashFileMap.txt') == 0:
               hashFileMap={}
            else:
               with open('hashFileMap.txt', 'rb') as f:
                   hashFileMap = pickle.load(f)
            Partition.hashFileMap = hashFileMap
            oldHashDisk = copy.deepcopy(Partition.hashDiskMap)
            oldBackupHashDisk = copy.deepcopy(Partition.hashDiskBackupMap)
            changedDisks = self.removeDisktoMap(diskToDel)
            changedBackupDisks = self.removeDisktoBackupMap(diskToDel)
            moveHashList = list(set(changedDisks) & set(Partition.hashFileMap.keys()))        
            moveBackupHashList = list(set(changedBackupDisks) & set(Partition.hashFileMap.keys()))
            migrateList = []
            migrateBackupList = []
            for k, v in Partition.hashFileMap.items():
                print(k, v)
                disk = Partition.hashDiskMap[k]
                print(Partition.diskIpMap[disk])
            for hashVal in moveHashList:
                print("Main Table Partition Details: ")
                newDisk = Partition.hashDiskMap[hashVal]
                oldDisk = oldHashDisk[hashVal]
                #print("newDisk:"+str(newDisk)+" oldDisk:"+str(oldDisk))
                fileList = Partition.hashFileMap[hashVal]
                newIpAdd = Partition.diskIpMap[newDisk]
                oldIpAdd = Partition.diskIpMap[oldDisk]
                print("Partition: "+str(hashVal)+" newIpAdd: "+str(newIpAdd) +" oldIp: "+str(oldIpAdd)+" FileNames: "+str(fileList))
                fileMigrate = FileMigrate(oldIpAdd, newIpAdd, fileList, hashVal)
                migrateList.append(fileMigrate)
            migrationData = pickle.dumps(migrateList)
            msg = struct.pack('>I', len(migrationData)) + migrationData
            conn.sendall(msg)
            #size = struct.pack('!I', len(migrationData))
            #conn.sendall(size) 
            #conn.send(migrationData)
            for hashVal in moveBackupHashList:
                print("Backup Table Partiton Details:")
                newBackupDisk =  Partition.hashDiskBackupMap[hashVal]
                oldBackupDisk = oldBackupHashDisk[hashVal]
               # print("bakup newDisk:"+str(newBackupDisk)+" oldDisk:"+str(oldBackupDisk))
                fileList = Partition.hashFileMap[hashVal]
                newBackupIpAdd = Partition.diskIpMap[newBackupDisk]
                oldBackupIpAdd = Partition.diskIpMap[oldBackupDisk]
                print("Partition: "+str(hashVal)+" newIpAdd:"+str(newBackupIpAdd) +" oldIp:"+str(oldBackupIpAdd)+" FileNames: "+str(fileList))
                fileMigrate = FileMigrate(oldBackupIpAdd, newBackupIpAdd, fileList, hashVal)
                migrateBackupList.append(fileMigrate)
            migrationBackupData = pickle.dumps(migrateBackupList)
            msg = struct.pack('>I', len(migrationBackupData)) + migrationBackupData
            conn.sendall(msg)
            #migrationBackupData = pickle.dumps(migrateBackupList)
            #conn.send(migrationBackupData)
            print(str(len(migrateBackupList)))
            
            #self.removeDisktoBackupMap(diskToDel)
            Partition.ipList.remove(ipAddress)
            if diskToDel in Partition.diskIpMap: del Partition.diskIpMap[diskToDel]
        else:
            conn.send("Not Found".encode('ascii'))
            
    def findDiskForIp(self, ipAddress):
        i=0
        while i< len(Partition.ipList):
            if Partition.ipList[i] == ipAddress:
                return i    
            i=i+1  
        return -1

    def removeDisktoMap(self, diskToDel):
        size = len(Partition.ipList)
        slots = int(Partition.rangeVal/(size-1))
        deletedSlots = list({k for k, v in Partition.hashDiskMap.items() if v == diskToDel})
        length = len(deletedSlots)
        print("list size: "+str(length)+"Partition.rangeVal"+str(Partition.rangeVal))
        i=0
        index = 0
        while i<size:
            if i!= diskToDel:
                slotCount = 1
                while slotCount <=slots:
                    #print("index "+str(index))
                    if index < length:
                      hashVal = deletedSlots[index]
                      Partition.hashDiskMap[hashVal] = i
                    slotCount = slotCount+1
                    index = index+1
            i=i+1
        deletedSlotsChk = list({k for k, v in Partition.hashDiskMap.items() if v == diskToDel})
        length = len(deletedSlotsChk)
        print("list size: "+str(length)+"Partition.rangeVal"+str(Partition.rangeVal))
        for hashV in deletedSlotsChk:
            Partition.hashDiskMap[hashVal] = Partition.ipList[0]
        return deletedSlots
        
    
    def removeDisktoBackupMap(self, diskToDel):
        size = len(Partition.ipList)
        slots = int(Partition.rangeVal/(size-1))
        deletedSlots = list({k for k, v in Partition.hashDiskBackupMap.items() if v == diskToDel})
        length = len(deletedSlots)
        print("list size: "+str(length))
        i=0
        index = 0
        while i<size:
            if i!= diskToDel:
                slotCount = 1
                while slotCount <=slots:
                    #print("index "+str(index))
                    if index < length:
                      hashVal = deletedSlots[index]
                      Partition.hashDiskBackupMap[hashVal] = i
                    slotCount = slotCount+1
                    index = index+1
            i=i+1
        deletedSlotsChk = list({k for k, v in Partition.hashDiskBackupMap.items() if v == diskToDel})
        length = len(deletedSlots)
        print("list size: "+str(length))
        for hashV in deletedSlotsChk:
            Partition.hashDiskBackupMap[hashVal] = Partition.ipList[0]
        return deletedSlots
