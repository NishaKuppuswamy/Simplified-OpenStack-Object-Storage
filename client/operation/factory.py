from operation.Upload import Upload
from operation.Download import Download
from operation.List import List
from operation.Delete import Delete
from operation.Add import Add
from operation.Remove import Remove
class OperationFactory(object):
    factoryClasses = {'upload':Upload,'download':Download,'list':List, 'delete':Delete, 'add':Add, 'remove':Remove}
    def createOperation(self, typ):
        if typ in OperationFactory.factoryClasses:
            return OperationFactory.factoryClasses[typ]()
        else:
            return "error"  
