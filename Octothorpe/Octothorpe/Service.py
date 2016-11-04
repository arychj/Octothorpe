import inspect, time
from abc import ABCMeta, abstractmethod
from importlib import import_module

from .Event import Event
from .Instruction import Instruction
from .Log import Log

class Service(metaclass=ABCMeta):
    _queue = None
    _instruction = None

    @property
    def _emitted_event_types(self):
        return []

    def Describe(self, method_name):
        method = getattr(self, method_name, None)
        if(method == None):
            return None
        else:
            return list(inspect.signature(method).parameters)

    def Emit(self, event_type, payload):
        if(event_type in self._emitted_event_types):
            Log.Debug(f"{self._instruction.Service}.{self._instruction.Method}() emitted event type '{event_type}'")

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
                instruction = Instruction(id, self._instruction.Level + 1, time.time(), "Test", method, payload)
                Service._queue.Enqueue(instruction)

    def Debug(self, message):
        Log.Debug(message)

    def Log(self, message):
        Log.Event(message)

    @staticmethod
    def Call(instruction):
        service_type = getattr(import_module(f".Services.{instruction.Service}", "Octothorpe"), instruction.Service)

        service = service_type()
        service._instruction = instruction

        method = getattr(service, instruction.Method, None)
        if(instruction.Payload == None):
            method()
        else:
            method(**instruction.Payload)
