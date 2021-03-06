from abc import ABCMeta, abstractmethod

from .DynamicModule import DynamicModule
from .Event import Event
from .Log import Log

class Shim(DynamicModule):

    @property
    def Name(self):
        return self._name

    @property
    def _module_type(self):
        return "shim"

    def __init__(self, service, name):
        self._service = service
        self._name = name

    def Inshimerate(self, event_type, payload):
        return self.CreateEvent(
            event_type,
            payload
        )  

    def Outshimerate(self, instruction):
        return instruction.Result

    def CreateEvent(self, event_type, payload):
        if(event_type in self._service._emitted_event_types):
            return Event.Create(
                None,
                self._service.Name,
                event_type,
                payload
            )
        else:
            Log.Error(f"Unknown event type '{event_type}' emitted by shim {self.Name}")
            return None

    @staticmethod
    def Get(service, name):
        if(name != None):
            shim_type = Shim._get_module("shim", name)
            shim = shim_type(service, name)
        else:
            shim = Shim(service, name)

        return shim
    