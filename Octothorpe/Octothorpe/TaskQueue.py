import threading, time, queue

from .Config import Config
from .Log import Log
from .Task import Task, TaskType, StopTask
from .TaskWorker import TaskWorker

class TaskQueue:
    _poll = True
    _queue = queue.PriorityQueue()

    @classmethod
    def Start(cls):
        for name in range(Config.GetInt("processing/worker_threads")):
            TaskWorker(cls, str(name))

        cls._start_polling()

    @classmethod
    def Stop(cls):
        Log.System("Stopping workers")

        cls._poll = False

        for _ in range(Config.GetInt("processing/worker_threads")):
            cls.Enqueue(StopTask())

    @classmethod
    def HasInstructions(cls):
        return (False if cls._queue.empty() else True)

    @classmethod
    def Enqueue(cls, task):
        if(task):
            if(task.TaskType != TaskType.Stop):
                Log.Debug(f"Queued task {task.Identity}")

            #check if has space, else db
            if(cls._queue.qsize() < 50):
                cls._queue.put(task)
            else:
                cls._queue.put(task)

    @classmethod
    def Dequeue(cls):
        return cls._queue.get(True)   

    @classmethod
    def Complete(cls):
        cls._queue.task_done()

    @classmethod
    def _start_polling(cls):
        cls._poll = True

        t = threading.Thread(target=cls._poll_for_tasks)
        t.start()

    @classmethod
    def _poll_for_tasks(cls):
        return

#        statement = Statement.Get("Instructions/GetQueued")
#        while(cls._poll):
#            result = statement.Execute({
#               "count": 50 - cls._queue.qsize()            
#            })
#
#            if(result.HasRows):
#                for row in rows:
#                    cls._queue.Enqueue(Instruction(
#                        row["Id"],
#                        row["Ident"],
#                        row["Level"],
#                       row["Service"],
#                       row["Method"],
#                       row["Payload"],
#                        row["GivenOn"],
#                        row["CompletedOn"]
#                    ))
#
#            time.sleep(1)

