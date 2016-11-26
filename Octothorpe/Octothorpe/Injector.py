import threading

from abc import ABCMeta, abstractmethod
from importlib import import_module

from .Config import Config
from .DynamicModule import DynamicModule
from .Instruction import Instruction
from .InstructionQueue import InstructionQueue
from .Log import Log
from .Shim import Shim

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

    def __init__(self, name, shim):
        self._name = name
        self._shim = shim

    def Inject(self, message):
        result = None

        shim = Shim.Get(self._shim)
        instruction = shim.Inbound(message)

        if(instruction):
            InstructionQueue.Enqueue(instruction)

            instruction.WaitUntilComplete()
            
            result = shim.Outbound(instruction)
        
        return result

    def Log(self, message):
        Log.System(message, tag=self._name)
            
    def Error(self, message):
        Log.Error(message, tag=self._name)
    
    @staticmethod
    def StartAll():
        xInjectors = Config._raw(f"injectors/injector")

        for xInjector in xInjectors:
            injector_type = Injector._get_module("injector", xInjector.attrib["name"])
            
            injector = injector_type(
                xInjector.attrib['name'],
                (xInjector.attrib['shim'] if "shim" in xInjector.attrib else None)
            )

            t = threading.Thread(target=injector.Start)
            t.daemon = True
            t.start()

            Injector._active_injectors.append(injector)

            Log.System(f"Injector '{injector._name}' started")

    @staticmethod
    def StopAll():
        Log.System("Stopping injectors")

        for injector in Injector._active_injectors:
            injector.Stop()
