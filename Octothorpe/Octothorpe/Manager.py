import sys, threading

from .InstructionQueue import InstructionQueue
from .Server import Server
from .Service import Service

class Manager:

    @staticmethod
    def Start():
        Service._queue = InstructionQueue

        InstructionQueue.Start()
        Server.Start()

    @staticmethod
    def Stop():
        InstructionQueue.Stop()
        Server.Stop()

    @staticmethod
    def Queue(instruction):
        InstructionQueue.Enqueue(instruction)

    @staticmethod
    def Process(instruction):
        Service.Call(instruction)

