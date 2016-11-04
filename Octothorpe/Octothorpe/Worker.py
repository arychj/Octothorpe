import time

from threading import Thread

from .Config import Config
from .Log import Log
from .Service import Service

class Worker(Thread):
    _queue = None
    _name = None

    def __init__(self, queue, name):
        Thread.__init__(self)
        
        self._queue = queue
        self._name = name
        self.start()

    def run(self):
        instruction = self._queue.Dequeue()
        while(instruction.Id != -1):
            try:
                Log.Debug(f"[{self._name}] processing instruction {instruction.Id}...")
                Service.Call(instruction)
            except Exception as e:
                Log.Exception(e)
            finally:
                instruction.Complete()
                self._queue.Complete()

            instruction = self._queue.Dequeue()
