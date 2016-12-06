import threading

from abc import ABCMeta, abstractmethod

from .Config import Config
from .DynamicModule import DynamicModule
from .Instruction import Instruction
from .Log import Log
from .Shim import Shim
from .TaskQueue import TaskQueue

#python circular dependency nonsensee
import Octothorpe.Event

class Injector(DynamicModule, metaclass=ABCMeta):
    _active_injectors = []
   
    @abstractmethod
    def _injector_start(self):
        pass

    @abstractmethod
    def _injector_stop(self):
        pass

    def Handle(self, handler, args=None, kwargs=None):
        t = threading.Thread(target=handler, args=args, kwargs=kwargs)
        t.start()

    def Inject(self, event_type, payload):
        result = None

        event = self._shim.Inshimerate(event_type, payload)

        if(event != None):
            TaskQueue.Enqueue(event)

            event.WaitUntilComplete()

            if(event.OutputInstruction != None):
                instruction = event.OutputInstruction

                instruction.WaitUntilComplete()

                result = self._shim.Outshimerate(instruction)
#                if(instruction.OutputTemplate != None):
#                    result = instruction.OutputTemplate.format(**instruction.Result)
#                else:
#                    result = instruction.Result

        return result

    def _create_event(self, event_type, payload):
        if(event_type in self._emitted_event_types):
            return Octothorpe.Event.Event.Create( #python circular dependency nonsense
                None,
                self.Name,
                event_type,
                payload
            )
        else:
            Log.Error(f"Unknown event type '{event_type}' emitted by shim {self.Name}")
            return None

    @staticmethod
    def StartAll():
        xInjectors = Config._raw(f"services/service[@injectable='true']")

        for xInjector in xInjectors:
            injector_type = Injector._get_module("service", xInjector.attrib["name"])
            
            injector = injector_type()
            injector._shim = Shim.Get(injector, xInjector.attrib['shim'] if "shim" in xInjector.attrib else None)

            t = threading.Thread(target=injector._injector_start)
            t.daemon = True
            t.start()

            Injector._active_injectors.append(injector)

            Log.System(f"Injector '{injector.Name}' started")

    @staticmethod
    def StopAll():
        Log.System("Stopping injectors")

        for injector in Injector._active_injectors:
            injector._injector_stop()
