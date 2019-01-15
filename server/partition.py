'''
Created on 09-Apr-2018

@author: nisha
'''
import hashlib
from command import Command
class Partition:
    '''
    classdocs
    '''

    diskMap = {}
    fileDiskMap = {}
    backupFileDiskMap={}
    partition = 0
    ipList = []
    diskIpMap = {}
    hashDiskMap = {}
    hashDiskBackupMap = {}
    hashFileMap = {}
    hashBackupFileMap = {}
    def __init__(self, *args, **kwargs):
        if len(args) == 2:
            Partition.partition = args[0]
            Partition.ipList = args[1]
            Partition.disks = len(args[1])
            self.updateDiskIpMap()
    
    def updateDiskIpMap(self):
        i=0
        for ip in Partition.ipList:
           Partition.diskIpMap[i] = ip
           i=i+1
    
    def findHash(self, userFileName):
        return self.calculateMD5(userFileName)
        
    def calculateMD5(self,filePath):
        hexDigit = hashlib.md5(filePath.encode('utf-8')).hexdigest()
        return hexDigit
    
    def findShiftedValue(self,hexValue, userFileName, partition):
        md5IntVal = int(str(hexValue),16)
        partition.findUpdateDisk(md5IntVal,userFileName)
        shiftVal = 128 - int(Partition.partition)
        remainder = md5IntVal>>shiftVal
        return remainder

    def updateDiskHashTable(self):
        partitionVal = 2. ** int(Partition.partition)
        rangeVal = partitionVal/Partition.disks
        Partition.rangeVal = rangeVal
        i=0
        actValue = 0
        while i<Partition.disks:
            Partition.diskMap[i] = actValue + rangeVal -1
            actValue = actValue + rangeVal
            i+=1

    
    def updateDiskHashTable1(self):
            partitionVal = 2. ** int(Partition.partition)
            rangeVal = int(partitionVal/Partition.disks)
            Partition.rangeVal = rangeVal
            i=0
            actValue = 0
            hashVal = 0
            while i<Partition.disks:
                maxValue = actValue + rangeVal -1
#                print("maxValue: "+str(maxValue))
                while hashVal <= maxValue:
                     Partition.hashDiskMap[hashVal] = i
 #                   print("hashVal: "+str(hashVal)+" disk: "+ str(i))
                     hashVal = hashVal+1
                actValue = actValue + rangeVal
                i+=1

    def updateDiskHashBackupTable1(self):
            partitionVal = 2. ** int(Partition.partition)
            i=0
            while i<partitionVal:
                    disk = Partition.hashDiskMap[i]
                    if disk == Partition.disks-1:
                        Partition.hashDiskBackupMap[i] = 0 
  #                     print("hashVal: "+str(i)+" disk: "+ str(0))
                    else:
                        Partition.hashDiskBackupMap[i] = disk+1
   #                    print("hashVal: "+str(i)+" disk: "+ str(disk+1))
                    i=i+1
        
    
    def findUpdateDisk(self,md5IntVal,userFileName):
        print("Partition.fileDiskMap:")
        for k, v in Partition.fileDiskMap.items():
             print(k, v)
        if userFileName not in Partition.fileDiskMap:
            print("userFile not found")
            shiftVal = 128 - int(Partition.partition) 
            remainder = md5IntVal>>shiftVal
            print("Hash: "+str(remainder))
            i=Partition.disks-1
            while i>0:
                if remainder <= Partition.diskMap[i] and remainder >= (Partition.diskMap[i-1]+1):
                    Partition.fileDiskMap[userFileName] = i;
                    #print(str(divmod(i+1,Partition.disks)))
                    #q,r = divmod(i+1,Partition.disks)
                    if i == Partition.disks-1:
                        Partition.backupFileDiskMap[userFileName] =  0
                    else:
                        Partition.backupFileDiskMap[userFileName] =  i+1
                    return Partition.fileDiskMap[userFileName]
                i=i-1
            if remainder < Partition.diskMap[1] and remainder > 0:
                    Partition.fileDiskMap[userFileName] = 0
                    Partition.backupFileDiskMap[userFileName] = 1
                    return Partition.fileDiskMap[userFileName]
        else:
            print("userFile found")
            Partition.backupFileDiskMap[userFileName] = Partition.fileDiskMap[userFileName] +1
            return Partition.fileDiskMap[userFileName] 
