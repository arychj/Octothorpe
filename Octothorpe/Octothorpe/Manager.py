import sys, threading

from .Config import Config
from .Instruction import Instruction
from .InstructionQueue import InstructionQueue
from .Log import Log
from .Server import Server
from .Worker import Worker

class Manager:
    _loop = True

    def Start(self):
        InstructionQueue.Start()
        Server.Start()

    def Stop(self):
        InstructionQueue.Stop()
        Server.Stop()

