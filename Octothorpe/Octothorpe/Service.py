import inspect, time
from abc import ABCMeta, abstractmethod
from importlib import import_module

from .Event import Event
from .Instruction import Instruction
#from .InstructionQueue import InstructionQueue

class Service(metaclass=ABCMeta):
    _queue = None
    _instruction = None

    @staticmethod
    def Process(queue, instruction):
        service_type = getattr(import_module(f".Services.{instruction.Service}", "Octothorpe"), instruction.Service)

        service = service_type()
        service._queue = queue
        service._instruction = instruction

        method = getattr(service, instruction.Method, None)
        if(instruction.Payload == None):
            method()
        else:
            method(**instruction.Payload)

    def Describe(self, method_name):
        method = getattr(self, method_name, None)
        if(method == None):
            return None
        else:
            return inspect.getargspec(method).args

    def Emit(self, event_type, payload):
        print("emit")

        event = Event(
            self._instruction,
            self.__class__.__name__, 
            event_type, 
            payload
        )

        #log event
        #get all rules that have hook on event
        #generate instruction for applicable services
        for method in ["Echo"]:
            #create instruction record
            id = 5000
            payload = event.Payload
            instruction = Instruction(id, self._instruction.Level + 1, time.time(), "Test", method, payload, False)
            self._queue.Enqueue(instruction)

