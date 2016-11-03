import sys, threading

from .Config import Config
from .Instruction import Instruction
from .InstructionQueue import InstructionQueue
from .Log import Log
from .Worker import Worker

class Manager:
    _loop = True

    def Start(self):
        InstructionQueue.Start()

        #t = threading.Thread(target=self.Loop)
        #t.start()

    def Stop(self):
        self._loop = False
        InstructionQueue.Stop()

    def Loop(self):
        instruction = InstructionQueue.Next()
        while(self._loop and (instruction.Id != -1) and Worker.IsAvailable()):
            try:
                Worker.Process(instruction)
                instruction = InstructionQueue.Next()
            except Exception as e:
                Log.Exception(e)

