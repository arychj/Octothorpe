from abc import ABCMeta, abstractmethod
from importlib import import_module

from EventQueue import EventQueue

class Service:
    @classmethod
    def Get(cls, name):
        service = getattr(import_module("Services." + name), name)
        return service()

    @abstractmethod
    def Process(self, event):
        return None

    def Emit(self, event):
        print("emit")
        EventQueue.Push(event)
