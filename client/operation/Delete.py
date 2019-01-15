'''
Created on 19-Apr-2018

@author: nisha
'''
from . import Operation
import os
import subprocess
class Delete(object):
    
    def executeOperation(self,s,commandClient):
            fileSplit = commandClient.processFileName()
            data = s.recv(1024)
           # data1 = s.recv(1024)
            if fileSplit == "error":
                 raise ValueError("Invalid Command. Enter Again.")
            deleteConf = input("Do you want to delete file. Enter \"yes\" to conform: ")
            if deleteConf and deleteConf == "yes":
                ips = str(data.decode('ascii'))
                ipsList = ips.split(" ")
                ipMachine = ipsList[0]
                backupIpMachine = ipsList[1]
                #ipMachine = str(data.decode('ascii'))
                print("Machine: "+ ipMachine)
                print("BackUp Machine: "+ backupIpMachine)
                self.deleteFromDirectory(s, fileSplit, ipMachine,False)
                self.deleteFromDirectory(s, fileSplit, backupIpMachine,True)
                    
    def deleteFromDirectory(self, s, fileSplit, ipMachine, isBackUp):
        try:
            directory = "/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"
            successMsg = "Deleted from machine "+ ipMachine+" \n "
            failureMsg = "Could not be deleted from " +ipMachine+ " \n "
            if isBackUp:
                sshCommand = "ssh " +os.getlogin()+"@"+ipMachine+" rm "+ "/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/backup_1_file_"+fileSplit[1]
            else:
                sshCommand = "ssh " +os.getlogin()+"@"+ipMachine+" rm "+ "/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"+fileSplit[1]
            errCode = os.system(sshCommand)
            if errCode == 0:
                isFileFound = "false"
                COMMAND="ls "+"/tmp/"+os.getlogin()+"/"+fileSplit[0]+"/"
                print(COMMAND)
                ssh = subprocess.Popen(["ssh", "%s" % ipMachine, COMMAND],
                                       shell=False,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                result = ssh.stdout.readlines()
                if result == []:
                    print(successMsg)
                    s.send(successMsg.encode('ascii'))
                else:
                    i=0
                    while i<len(result):
                       eachResult = str(result[i])
                       if eachResult == fileSplit[1]:
                           isFileFound = "true"    
                       i=i+1
                
                if isFileFound == "false":
                    print(successMsg)
                    s.send(successMsg.encode('ascii'))
                else:
                    print(failureMsg)
                    s.send(failureMsg.encode('ascii'))
            else:
                 print(failureMsg)
                 s.send(failureMsg.encode('ascii'))
        except SSHException as e:
             print(failureMsg)
             s.send(failureMsg.encode('ascii'))
             print(str(e))
        except OSError as e:
             print(failureMsg)
             s.send(failureMsg.encode('ascii'))
             print(str(e))
