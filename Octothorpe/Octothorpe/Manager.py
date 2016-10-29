import time

from .Config import Config
from .InstructionQueue import InstructionQueue
from .Log import Log
from .Worker import Worker

class Manager:
    def Start(self):
        InstructionQueue.blah()
        InstructionQueue.StartPolling()
        self.Loop()

    def Loop(self):
        while(True):
            instruction = InstructionQueue.Next()
            try:
                while((instruction != None) and Worker.IsAvailable()):
                    Worker.Process(instruction)
                    instruction = InstructionQueue.Next()
            except Exception as e:
                Log.Exception(e)

