import threading

from .Config import Config
from .InstructionQueue import InstructionQueue
from .Log import Log
from .Worker import Worker

class Manager:
    _loop = True

    def Start(self):
        InstructionQueue.blah()
        InstructionQueue.StartPolling()

        t = threading.Thread(target=self.Loop)
        t.start()

    def Stop(self):
        self._loop = False
        InstructionQueue.Push(None)
        InstructionQueue.StopPolling()

    def Loop(self):
        while(self._loop):
            instruction = InstructionQueue.Next()
            try:
                while(self._loop and (instruction != None) and Worker.IsAvailable()):
                    Worker.Process(instruction)
                    instruction = InstructionQueue.Next()
            except Exception as e:
                Log.Exception(e)

