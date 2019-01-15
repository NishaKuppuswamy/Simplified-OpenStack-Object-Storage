from operation.Upload import Upload
from operation.Download import Download
from operation.List import List
from operation.Delete import Delete
from operation.Remove import Remove
from operation.Add import Add
class OperationFactory(object):
    factoryClasses = {'upload':Upload,'download':Download,'list':List, 'delete':Delete, 'add':Add, 'remove':Remove}
    def createOperation(self, typ):
       return OperationFactory.factoryClasses[typ]()
   
   
