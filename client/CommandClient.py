'''
Created on 09-Apr-2018

@author: nisha
'''
import os
import subprocess
import socket

class CommandClient(object):


    def __init__(self, command):
        self.command = command
    
    def processClient(self):
        if self.command:
            commandSplits = self.command.split(" ")   
            if commandSplits:
                return commandSplits[0],commandSplits[1]    

    def processCommand(self):
        if self.command:
            commandSplits = self.command.split(" ")   
            if commandSplits and len(commandSplits) == 2:  
                return commandSplits[0],commandSplits[1]
            else:
                return "error",""
        else:
            return "error",""
               
    def processClientCommand(self):
        if self.command:
            commandSplits = self.command.split(" ")   
            if commandSplits and len(commandSplits) == 3:
                return commandSplits[1], commandSplits[2]

    def processHost(self, host):
        if host.count('.') == 3:
           return host
        else:
           ip = socket.gethostbyname(host)
           return ip
                    
    def processFileName(self): 
        print("processFileName:"+ self.command) 
        commandSplits = self.command.split(" ")
        if commandSplits[1] and "/" in commandSplits[1]:
            userFile = commandSplits[1].split("/")       
            return userFile
        else:
            return "error"
   
    def processIpAddress(self):
        commandSplits = self.command.split(" ")
        if commandSplits[1] and commandSplits[1].count('.') == 3:
           ipSplits = commandSplits[1].split(".")
           if len(ipSplits) != 4:
               return "error"
        else:
            return "error"    
     
                        
    def processUploadForServer(self):  
        commandSplits = self.command.split(" ")
        commandSplitSecond = commandSplits[1].split("/")       
        if commandSplitSecond:
             # return "/tmp/"+commandSplitSecond[0]+"/C0/"+commandSplitSecond[1], commandSplitSecond[1]
             for root, dirs, files in os.walk("C:\SCU\Interview"):  # @UnusedVariable
                for file in files:
                        if file == "Notes.txt":
                            print("File Found")
                            return "C:/SCU/Interview/Notes.txt", commandSplitSecond[1]
                        
    def processList(self,ipList,user):
        msg = ""
        i=0
        print("inside processList")
        while i<len(ipList):
            HOST=ipList[i]
            #print(HOST)
            msg1 = "Disk"+str(i)+": "+ipList[i]
            print("Disk"+str(i)+": "+ipList[i])
            msg = msg+msg1+"%"
            COMMAND="ls -lrt"+" /tmp/"+os.getlogin()+"/"+user+"/ -I \"backup_1_file_*\"" 
            ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                  shell=False,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE)
            result = ssh.stdout.readlines()
            
            if result != []:
                #msg1 = "Disk"+str(i)+": "+ipList[i]
               # print("Disk"+str(i)+": "+ipList[i])
               # msg = msg+msg1+"%"
                j=1
                while j<len(result):
                   eachResult = str(result[j])
                   print(eachResult[2:-3])
                   msg2 = eachResult[2:-3]
                   msg = msg+msg2+"%"
                   j=j+1
            i=i+1
        return msg 
             

    def processIp(self,ipListString):
        ipList = ipListString.split(" ")
        return ipList
