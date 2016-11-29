from threading import Thread

from .Config import Config
from .Log import Log
from .Task import TaskType

class Worker(Thread):
    _name = None

    def __init__(self, queue, name):
        Thread.__init__(self)
        
        self._queue = queue
        self._name = name
        self.start()

    def run(self):
        task = self._queue.Dequeue()
        while(task.TaskType != TaskType.Stop):
            try:
                Log.Debug(f"Started processing task {task.Identity}...", tag=self._name)

                task.Processing()
                task.Process()
                task.Complete()

                Log.Debug(f"Finished processing task {task.Identity} in {task.ProcessingTime:.3f} seconds (waited {task.WaitingTime:.3f})", tag=self._name)
            except Exception as e:
                task.Fail()
                Log.Exception(e)
            finally:
                self._queue.Complete()

            task = self._queue.Dequeue()

        Log.Debug("Stopping", tag=self.name)
