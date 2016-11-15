import inspect, time
from abc import ABCMeta, abstractmethod
from functools import lru_cache
from importlib import import_module

from .Config import Config
from .DynamicModule import DynamicModule
from .Event import Event
from .Instruction import Instruction
from .Log import Log
from .Rule import Rule

class Service(DynamicModule, metaclass=ABCMeta):
    _queue = None
    _instruction = None

    @property
    def _module_type(self):
        return "service"

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
        if((event_type == self._instruction.Method) or (event_type in self._emitted_event_types)):
            Log.Debug(f"Event '{event_type}' emitted by {self._instruction.Service}.{self._instruction.Method}()")

            event = Event.Create(
                self._instruction,
                self.__class__.__name__, 
                event_type, 
                payload
            )

            rules = Rule.GetMatches(event)
            for rule in rules:
                instruction = Instruction.Create(
                    self._instruction.Level + 1, 
                    rule.ConsumingService, 
                    rule.ConsumingMethod, 
                    rule.PreparePayload(event)
                )

                Service._queue.Enqueue(instruction)
        else:
            Log.Error(f"Unknown event type '{event_type}' emitted by service {self._instruction.Service}.{self._instruction.Method}()")

    def Log(self, message):
        Log.Entry(message)

    @staticmethod
    def Call(instruction):
        instruction.Processing()

        service_type = Service._get_module("service", instruction.Service)

        service = service_type()
        service._instruction = instruction

        method = getattr(service, instruction.Method, None)
        if(instruction.Payload == None):
            instruction.Result = method()
        else:
            instruction.Result = method(**instruction.Payload)

        if(instruction.Result != None):
            service.Emit(f"{instruction.Method}", instruction.Result)

