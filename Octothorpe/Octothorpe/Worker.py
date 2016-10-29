import threading, time

from .Config import Config
from .Log import Log
from .Service import Service

class Worker:
    _lock = threading.Lock()
    _active_workers = 0

    @classmethod
    def IsAvailable(cls):
        while(cls._active_workers >= Config.GetInt("processing/max_workers")):
            time.sleep(0.1)

        return True

    @classmethod
    def Count(cls):
        return cls._active_workers

    @classmethod
    def Process(cls, instruction):
        with cls._lock:
            cls._active_workers += 1

        t = threading.Thread(target=cls.Run, args=(instruction,))
        t.start()
    
    @classmethod
    def Run(cls, instruction):
        try:
            service = Service.Get(instruction.Service)
            service.Process(instruction)
        except Exception as e:
            Log.Exception(e)
        finally:
            instruction.Complete()
            cls.End()

    @classmethod
    def End(cls):
        with cls._lock:
            cls._active_workers -= 1
