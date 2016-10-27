import threading, time

from Config import Config
from Log import Log
from Service import Service

class Worker:
    lock = threading.Lock()
    active_workers = 0

    @classmethod
    def IsAvailable(cls):
        while(cls.active_workers >= Config.GetInt("processing/max_workers")):
            time.sleep(0.1)

        return True

    @classmethod
    def Count(cls):
        return cls.active_workers

    @classmethod
    def Process(cls, event):
        with cls.lock:
            cls.active_workers += 1

        t = threading.Thread(target=cls.Run, args=(event,))
        t.start()
    
    @classmethod
    def Run(cls, event):
        try:
            service = Service.Get(event.service)
            service.Process(event)
        except Exception as e:
            Log.Exception(e)
        finally:
            event.Complete()
            cls.End()

    @classmethod
    def End(cls):
        with cls.lock:
            cls.active_workers -= 1
