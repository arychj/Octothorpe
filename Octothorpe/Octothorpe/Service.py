import inspect, time
from abc import ABCMeta, abstractmethod
from functools import lru_cache
from importlib import import_module

from .Config import Config
from .DynamicModule import DynamicModule
from .Event import Event
from .Log import Log
from .TaskQueue import TaskQueue

class Service(DynamicModule, metaclass=ABCMeta):
    @property
    def _module_type(self):
        return "service"
    
    @property
    def _name(self):
        return self.__class__.__name__

    @property
    def _emitted_event_types(self):
        return []

    @property
    def _event_type_default(self):
        return f"_{self._instruction.Method.lower()}"

    def Describe(self, method_name):
        method = getattr(self, method_name, None)
        if(method == None):
            return None
        else:
            return list(inspect.signature(method).parameters)

    def Emit(self, event_type, payload):
        if((event_type == self._event_type_default) or (event_type in self._emitted_event_types)):
            Log.Debug(f"Event '{event_type}' emitted by {self._instruction.Service}.{self._instruction.Method}()")

            event = Event.Create(
                self._instruction,
                self.__class__.__name__, 
                event_type, 
                payload
            )

            TaskQueue.Enqueue(event)
        else:
            Log.Error(f"Unknown event type '{event_type}' emitted by service {self._instruction.Service}.{self._instruction.Method}()")

    def Log(self, message):
        Log.Entry(message)

    def Error(self, message):
        Log.Error(message, tag=self._name)

    @staticmethod
    def Call(instruction):
        service_type = Service._get_module("service", instruction.Service)

        service = service_type()
        service._instruction = instruction

        method = getattr(service, instruction.Method, None)
        if(method != None):
            if(instruction.Payload == None):
                instruction.Result = method()
            else:
                instruction.Result = method(**instruction.Payload)

            if(instruction.Result != None):
                service.Emit(service._event_type_default, instruction.Result)
        else:
            Log.Error(f"Unknown method '{instruction.Method}' in '{instruction.Service}'")

