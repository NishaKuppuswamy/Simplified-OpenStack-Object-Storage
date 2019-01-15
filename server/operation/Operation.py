'''
Created on 19-Apr-2018

@author: nisha
'''
from abc import ABCMeta, abstractmethod

class Operation(metaclass=ABCMeta):
   @abstractmethod
   def executeOperation(self,s,commandClient):
        pass