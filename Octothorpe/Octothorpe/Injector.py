import threading, time

from abc import ABCMeta, abstractmethod
from importlib import import_module

from .Config import Config
from .Instruction import Instruction
from .InstructionQueue import InstructionQueue
from .Log import Log

class Injector(metaclass=ABCMeta):
    
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
        Log.System(f"[{self._name}] {message}")

    def GetSetting(self, key):
        return self.GetSettings(key)[0].text

    def GetSettings(self, key):
        return Config._raw(f"injectors/injector[@name='{self._name}']/{key}")
            
    @staticmethod
    def StartAll():
        xInjectors = Config._raw(f"injectors/injector")

        for xInjector in xInjectors:
            injector_type = Injector._get_injector(xInjector.attrib['name'])
            
            injector = injector_type()
            injector._name = xInjector.attrib['name']
            t = threading.Thread(target=injector.Start)
            t.start()

            Log.System(f"Injector '{injector._name}' started")

    @staticmethod
    def StopAll():
        pass

    @staticmethod
    def _get_injector(name):
        return getattr(import_module(f".Injectors.{name}", "Octothorpe"), name[name.find('.') + 1:])

