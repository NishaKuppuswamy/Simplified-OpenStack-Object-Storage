'''
Created on 19-Apr-2018

@author: nisha
'''
import os
import logging
#from . import Operation

class Upload(object):
    
    def executeOperation(self,s,commandClient):
        fileSplit = commandClient.processFileName()
        data = s.recv(1024)
        #data1 = s.recv(1024)
        if fileSplit == "error":
            raise ValueError("Invalid Command. Enter Again.")
        ips = str(data.decode('ascii'))
        ipsList = ips.split(" ")
        ipMachine = ipsList[0]
        backupIpMachine = ipsList[1]
        print("Machine: "+ str(data.decode('ascii')))
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        isFileFound = "false"
        for file in files:
            if file == fileSplit[1]:
                isFileFound = "true" 
        if isFileFound == "false":
            raise ValueError("File not in location:"+ "/P1/client/")
        try:
            sshCommand = "ssh " +os.getlogin()+"@"+ipMachine+" \"mkdir -p "+ "/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/\""
            scpCommand = "scp -B "+fileSplit[1]+" "+os.getlogin()+"@"+ipMachine+":/tmp/"+os.getlogin()+"/"+fileSplit[0]
            os.system(sshCommand)
            os.system(scpCommand)
            sshCommand = "ssh " +os.getlogin()+"@"+backupIpMachine+" \"mkdir -p "+ "/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/\""
            scpCommand = "scp -B "+fileSplit[1]+" "+os.getlogin()+"@"+backupIpMachine+":/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/backup_1_file_"+fileSplit[1]
            os.system(sshCommand)
            os.system(scpCommand)
            msgIp = "File located at: "+ipMachine+": /tmp/"+os.getlogin()+"/"+fileSplit[0]
            msgBkUp = "File located at: "+backupIpMachine+": /tmp/"+os.getlogin()+"/"+fileSplit[0]
            msgIp = msgIp +"%"+msgBkUp
            print("File located at: "+ipMachine+": /tmp/"+os.getlogin()+"/"+fileSplit[0])
            print("File located at: "+backupIpMachine+": /tmp/"+os.getlogin()+"/"+fileSplit[0])
            s.send(msgIp.encode('ascii'))
        except OSError as e:
            logging.error(str(e))
