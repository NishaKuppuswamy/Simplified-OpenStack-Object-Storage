'''
Created on 09-Apr-2018

@author: nisha
'''
import socket
class Command(object):
    '''
    classdocs
    '''
    ipList = []
    def __init__(self, command):
        self.command = command
        
    def processCommand(self):
        if self.command:
            commandSplits = self.command.split(" ")   
            if commandSplits:
                return commandSplits[0]

    def processServerCommand(self):
        commandSplits = self.command.split(" ")
        partition = commandSplits[1]
        i = 2
        while i < len(commandSplits):
           if commandSplits[i].count('.') == 3:
              Command.ipList.append(commandSplits[i])
              i+=1
           else:
              print(str(commandSplits[i]))
              ip = socket.gethostbyname(commandSplits[i])
              Command.ipList.append(str(ip))
              print("HostName:"+commandSplits[i]+" IP:"+str(ip))
              i+=1
        return partition,Command.ipList 
    
    def getFullFilePath(self,userFileName):
        fileNameSplit = userFileName.split("/")       
        if fileNameSplit:
              return fileNameSplit[1]   
                        
    def processUploadForServer(self):  
        commandSplits = self.command.split(" ")
        commandSplitSecond = commandSplits[1].split("/")       
        if commandSplitSecond:
            return commandSplits[1]
        
    def getIpfromCommand(self):
        commandSplits = self.command.split(" ")
        if commandSplits[1]:
            return commandSplits[1]

    def getUserNamefromCommand(self):
        commandSplits = self.command.split(" ")
        if commandSplits[1]:
            return commandSplits[1]

    def processDownload(self):
        print(self.command)
        commandSplits = self.command.split(" ")
        commandSplitSecond = commandSplits[1].split("/")       
        if commandSplitSecond:
            return commandSplits[1]
