import threading, time, queue

from .Config import Config
from .Instruction import Instruction
from .Worker import Worker

class InstructionQueue:
    _poll = True
    _queue = queue.PriorityQueue()

    @classmethod
    def Start(cls):
        for name in range(Config.GetInt("processing/worker_threads")):
            Worker(cls, str(name))

        cls._start_polling()

    @classmethod
    def Stop(cls):
        cls._poll = False

        for _ in range(Config.GetInt("processing/worker_threads")):
            cls.Enqueue(Instruction.GetStopInstruction())

    @classmethod
    def HasInstructions(cls):
        return (False if cls._queue.empty() else True)

    @classmethod
    def Enqueue(cls, instruction):
        #check if has space, else db
        if(cls._queue.qsize() < 50):
            cls._queue.put(instruction)
        else:
            pass

    @classmethod
    def Dequeue(cls):
        return cls._queue.get(True)   

    @classmethod
    def Complete(cls):
        cls._queue.task_done()

    @classmethod
    def _start_polling(cls):
        cls._poll = True

        t = threading.Thread(target=cls._poll_for_instructions)
        t.start()

    @classmethod
    def _poll_for_instructions(cls):
        return

        statement = Statement.Get("Instructions/GetQueued")
        while(cls._poll):
            result = statement.Execute({
               "count": 50 - cls._queue.qsize()            
            })

            if(result.HasRows):
                for row in rows:
                    cls._queue.Enqueue(Instruction(
                        row["Id"],
                        row["Ident"],
                        row["Level"],
                        row["Service"],
                        row["Method"],
                        row["Payload"],
                        row["GivenOn"],
                        row["CompletedOn"]
                    ))

            time.sleep(1)

