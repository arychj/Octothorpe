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
                Log.Debug(f"Started processing instruction {instruction.Id}...", tag=self._name)

                Service.Call(instruction)
                instruction.Complete()

                Log.Debug(f"Finished processing instruction {instruction.Id} in {instruction.ProcessingTime:.2f} seconds (waited {instruction.WaitingTime:.2f})", tag=self._name)
            except Exception as e:
                instruction.Fail()
                Log.Exception(e)
            finally:
                self._queue.Complete()

            instruction = self._queue.Dequeue()

        Log.Debug("Stopping", tag=self.name)
