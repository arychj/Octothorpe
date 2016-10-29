from abc import ABCMeta, abstractmethod
from importlib import import_module

from .Event import Event
from .Instruction import Instruction
from .InstructionQueue import InstructionQueue

class Service(metaclass=ABCMeta):
    @classmethod
    def Get(cls, name):
        service = getattr(import_module(f".Services.{name}", "Octothorpe"), name)
        return service()

    @abstractmethod
    def Process(self, instruction):
        pass

    def Emit(self, event_type, instruction, payload):
        print("emit")

        event = Event(
            instruction,
            self.__class__.__name__, 
            event_type, 
            payload
        )

        #log event
        #get all rules that have hook on event
        #generate instruction for applicable services
        for service in ["Echo"]:
            #create instruction record
            id = 5000
            payload = event.Payload
            instruction = Instruction(id, service, payload)
            InstructionQueue.Push(instruction)

