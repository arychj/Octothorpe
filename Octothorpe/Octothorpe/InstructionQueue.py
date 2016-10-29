import threading, time, queue

from .Instruction import Instruction

from random import randint

class InstructionQueue:
    _poll = True
    _queue = queue.Queue(50)

    @classmethod
    def blah(cls):
        for i in range(50):
            payload = "*" * i
            instruction = Instruction(i, ("Echo" if randint(0,1) == 0 else "Test"), payload)
            cls.Push(instruction)
        
    @classmethod
    def HasInstructions(cls):
        return (False if cls._queue.empty() else True)

    @classmethod
    def Push(cls, instruction):
        cls._queue.put(instruction, True)

    @classmethod
    def Next(cls):
        return cls._queue.get(True)

    @classmethod
    def StartPolling(cls):
        t = threading.Thread(target=cls.PollForInstructions)
        t.start()
        
    @classmethod
    def PollForInstructions(cls):
        while(cls._poll):
            x = 1
            time.sleep(1)

