import threading, time, queue

from .Instruction import Instruction
from .Worker import Worker

class InstructionQueue:
    _poll = True
    _queue = queue.PriorityQueue()

    @classmethod
    def Start(cls):
        for name in range(5):
            Worker(cls, name)

        cls._start_polling()

    @classmethod
    def Stop(cls):
        cls._poll = False

        for _ in range(5):
            cls.Enqueue(Instruction.GetStopInstruction())

    @classmethod
    def HasInstructions(cls):
        return (False if cls._queue.empty() else True)

    @classmethod
    def Enqueue(cls, instruction):
        #check if has space, else db

        cls._queue.put(instruction)

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
        while(cls._poll):
            #get queue size up to 50
            time.sleep(1)

