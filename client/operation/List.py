'''
Created on 19-Apr-2018

@author: nisha
'''
import pickle
import os
import logging
class List(object):
    
    def executeOperation(self,s,commandClient):
            command,user= commandClient.processClient()
            data1 = s.recv(2048)
            ipListString = data1.decode('ascii')
            #print(ipListString)
            ipList = commandClient.processIp(ipListString)
            #print("Ip List: "+ str(ipList))
            data = s.recv(8192)
            migrationList = pickle.loads(data)
            try:
                if migrationList:
                   print("Processing..")
                for migrationObj in migrationList:
                    #oldIp = migrationObj.oldIp
                    
                    mainIp = migrationObj.mainIp
                    backupIp = migrationObj.backupIp
                    filename = migrationObj.filename
                    sshCommand = "ssh " +mainIp+" test -f "+"\"/tmp/"+os.getlogin()+"/"+user+"/"+filename+"\"" 
                    #print(sshCommand)
                    errCode = os.system(sshCommand)
                    if errCode != 0:
                        #print("not in main ip")
                        scpCommand ="ssh "+os.getlogin()+"@"+mainIp+ " \" mkdir -p /tmp/"+os.getlogin()+"/"+user+"/ && touch /tmp/"+os.getlogin()+"/"+user+"/"+filename+"\" && " +"scp -B "+os.getlogin()+"@"+mainIp+":/tmp/"+os.getlogin()+"/"+user+"/"+filename+ " "+os.getlogin()+"@"+backupIp+":/tmp/"+os.getlogin()+"/"+user+"/backup_1_file_"+filename                    
                        #print(scpCommand)
                        sshCommand = "ssh " +backupIp+" test -f "+"\"/tmp/"+os.getlogin()+"/"+user+"/backup_1_file_"+filename+"\"" 
                        #print(sshCommand)
                        errCode = os.system(sshCommand)
                        if errCode == 0:
                            #print("present in backup")
                            os.system(scpCommand)
                    else:
                        sshCommand = "ssh " +backupIp+" test -f "+"\"/tmp/"+os.getlogin()+"/"+user+"/backup_1_file_"+filename+"\"" 
                        #print(sshCommand)
                        errCode = os.system(sshCommand)
                        if errCode != 0:
                           #print("not in backup")
                           scpCommand = "ssh "+os.getlogin()+"@"+backupIp+ " \" mkdir -p /tmp/"+os.getlogin()+"/"+user+"/ && touch /tmp/"+os.getlogin()+"/"+user+"/backup_1_file_"+filename+"\" && " + "scp -B "+os.getlogin()+"@"+backupIp+":/tmp/"+os.getlogin()+"/"+user+"/backup_1_file_"+filename+ " "+os.getlogin()+"@"+mainIp+":/tmp/"+os.getlogin()+"/"+user+"/"+filename 
                           #print(scpCommand)
                           sshCommand = "ssh " +mainIp+" test -f "+"\"/tmp/"+os.getlogin()+"/"+user+"/"+filename+"\"" 
                           #print(sshCommand)
                           errCode = os.system(sshCommand)
                           if errCode == 0:
                               #print("present in main")
                               os.system(scpCommand)
                msg = commandClient.processList(ipList,user)   
                if msg == '':
                        print("no files to display")
                        msg = "no files to display" 
                        s.send(msg.encode('ascii'))
                else:
                        s.send(msg.encode('ascii'))
            except OSError as e:
                logging.error(str(e))

