from abc import ABCMeta, abstractmethod

from .DynamicModule import DynamicModule
from .Instruction import Instruction
from .Log import Log

class Shim(DynamicModule):

    @property
    def _module_type(self):
        return "shim"

    def __init__(self, name):
        self._name = name

    def Inbound(self, message):
        return Instruction.Parse(message)        

    def Outbound(self, instruction):
        return str(instruction.Result)

    @classmethod
    def CreateInstruction(cls, service, method, payload):
        return Instruction.Create(
            1,
            service,
            method,
            payload
        )

    @staticmethod
    def Get(name):
        if(name != None):
            shim_type = Shim._get_module("shim", name)
            shim = shim_type(name)
        else:
            shim = Shim(name)

        return shim
    