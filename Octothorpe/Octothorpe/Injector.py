import threading

from abc import ABCMeta, abstractmethod

from .Config import Config
from .DynamicModule import DynamicModule
from .Instruction import Instruction
from .Log import Log
from .TaskQueue import TaskQueue
from .Shim import Shim

class Injector(DynamicModule, metaclass=ABCMeta):
    _active_injectors = []
   
    @abstractmethod
    def Start(self):
        pass

    @abstractmethod
    def Stop(self):
        pass

    def __init__(self, shim):
        self._shim = shim

    def Handle(self, handler, args=None, kwargs=None):
        t = threading.Thread(target=handler, args=args, kwargs=kwargs)
        t.start()

    def Inject(self, message):
        result = None

        shim = Shim.Get(self._shim)
        instruction = shim.Inbound(message)

        if(instruction):
            TaskQueue.Enqueue(instruction)

            instruction.WaitUntilComplete()
            
            result = shim.Outbound(instruction)
        
        return result

    @staticmethod
    def StartAll():
        xInjectors = Config._raw(f"services/service[@injectable='true']")

        for xInjector in xInjectors:
            injector_type = Injector._get_module("service", xInjector.attrib["name"])
            
            injector = injector_type(
                (xInjector.attrib['shim'] if "shim" in xInjector.attrib else None)
            )

            t = threading.Thread(target=injector.Start)
            t.daemon = True
            t.start()

            Injector._active_injectors.append(injector)

            Log.System(f"Injector '{injector.Name}' started")

    @staticmethod
    def StopAll():
        Log.System("Stopping injectors")

        for injector in Injector._active_injectors:
            injector.Stop()
