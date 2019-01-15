'''
Created on 04-May-2018

@author: nisha
'''

class FileMigrate(object):
    '''
    classdocs
    '''


    def __init__(self, oldIp=None, newIp=None, fileList=None, hashVal=None):
        self.oldIp  = oldIp
        self.newIp = newIp
        self.fileList = fileList
        self.hashVal = hashVal
        
    def updateIpDetails(self, mainIp, backupIp, filename):
        self.mainIp = mainIp
        self.backupIp = backupIp
        self.filename = filename
        
        
