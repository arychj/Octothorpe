import threading, time, queue

from .Instruction import Instruction

class InstructionQueue:
    _poll = True
    _queue = queue.PriorityQueue()
        
    @classmethod
    def HasInstructions(cls):
        return (False if cls._queue.empty() else True)

    @classmethod
    def Queue(cls, instruction):
        cls._queue.put(instruction, True)

    @classmethod
    def Next(cls):
        return cls._queue.get(True)

    @classmethod
    def StartPolling(cls):
        cls._poll = True

        t = threading.Thread(target=cls.PollForInstructions)
        t.start()

    @classmethod
    def StopPolling(cls):
        cls._poll = False
                
    @classmethod
    def PollForInstructions(cls):
        while(cls._poll):
            #get queue size up to 50
            time.sleep(1)

