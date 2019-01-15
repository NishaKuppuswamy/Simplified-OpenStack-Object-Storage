'''
Created on 19-Apr-2018

@author: nisha
'''
from . import Operation
import os
from os.path import abspath, exists
class Download(object):
    
    def executeOperation(self,s,commandClient):
        fileSplit = commandClient.processFileName()
        data = s.recv(1024)
#        data1 = s.recv(1024)
        if fileSplit == "error":
             raise ValueError("Invalid Command. Enter Again.")
        ips = str(data.decode('ascii'))
        ipsList = ips.split(" ")
        ipMachine = ipsList[0]
        backupIpMachine = ipsList[1]
        #ipMachine = str(data.decode('ascii'))
        print("Machine: "+ str(data.decode('ascii')))
        print("BackUp Machine: "+ backupIpMachine)
       # directory = "/P11/client/"
       # if not os.path.exists(directory):
       #     os.makedirs(directory)
        scpCommand = "scp -B "+os.getlogin()+"@"+ipMachine+":/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"+fileSplit[1]+" ."
        errorCode = os.system(scpCommand)
        print(scpCommand)
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        isFileFound = "false"
        for file in files:
            if file == fileSplit[1]:
                isFileFound = "true"
   
       # for root, dirs, files in os.walk(directory):
       #     for file in files:
       #             if file == fileSplit[1]:
       #                isFileFound = "true" 
        if isFileFound == "true" and errorCode == 0:
            msg = "Downloaded successfully to /P1/cloud folder!!"
            print(msg)
            f_path = abspath(fileSplit[1])
            if exists(f_path):
                with open(f_path) as f:
                    print(f.read())
            s.send(msg.encode('ascii')) 
        #backupIpMachine = str(data1.decode('ascii'))
#        print("Backup Machine: "+ str(data1.decode('ascii')))
        else:
            scpCommand = "scp -B "+os.getlogin()+"@"+backupIpMachine+":/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/backup_1_file_"+fileSplit[1]+" ."
            errorCode = os.system(scpCommand)
            os.rename("backup_1_file_"+fileSplit[1],fileSplit[1])
           # for root, dirs, files in os.walk(directory):
            #    for file in files:
             #           if file == fileSplit[1]:
              #             isFileFound = "true"
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            isFileFound = "false"
            for file in files:
                if file == "/backup_1_file_"+fileSplit[1]:
                    isFileFound = "true"
            if isFileFound == "true" and errorCode == 0:
                msg = "Downloaded successfully to /P1/cloud folder!!"
                print(msg)
                s.send(msg.encode('ascii'))
                f_path = abspath(fileSplit[1])
                if exists(f_path):
                    with open(f_path) as f:
                        print(f.read())
            else:
                msg = "Download Unsuccessfull"
                print(msg)
                s.send(msg.encode('ascii'))   
