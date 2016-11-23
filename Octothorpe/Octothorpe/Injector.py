import threading, time

from abc import ABCMeta, abstractmethod
from importlib import import_module

from .Config import Config
from .DynamicModule import DynamicModule
from .Instruction import Instruction
from .InstructionQueue import InstructionQueue
from .Log import Log

class Injector(DynamicModule, metaclass=ABCMeta):
    _active_injectors = []
   
    @property
    def _module_type(self):
        return "injector"

    @abstractmethod
    def Start(self):
        pass

    @abstractmethod
    def Stop(self):
        pass

    def Call(self, service, method, payload):
        instruction = Instruction.Create(
            1,
            service,
            method,
            payload
        )

        InstructionQueue.Enqueue(instruction)

        while(instruction.IsComplete == False):
            time.sleep(0.1)
        
        return instruction.Result

    def Log(self, message):
        Log.System(message, tag=self._name)
            
    @staticmethod
    def StartAll():
        xInjectors = Config._raw(f"injectors/injector")

        for xInjector in xInjectors:
            #module_name = (xInjector.attrib["module"] if ('module' in xInjector.attrib) else xInjector.attrib["name"])
            injector_type = Injector._get_module("injector", xInjector.attrib["name"])
            
            injector = injector_type()
            injector._name = xInjector.attrib['name']
            t = threading.Thread(target=injector.Start)
            t.start()

            Injector._active_injectors.append(injector)

            Log.System(f"Injector '{injector._name}' started")

    @staticmethod
    def StopAll():
        for injector in Injector._active_injectors:
            injector.Stop()

