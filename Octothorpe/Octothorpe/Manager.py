import sys, threading

from .Injector import Injector
from .InstructionQueue import InstructionQueue
from .Log import Log
from .Service import Service

class Manager:

    @staticmethod
    def Start():
        Service._queue = InstructionQueue

        InstructionQueue.Start()
        Injector.StartAll()

    @staticmethod
    def Stop():
        Log.System("Stopping system")

        InstructionQueue.Stop()
        Injector.StopAll()

    @staticmethod
    def Queue(instruction):
        InstructionQueue.Enqueue(instruction)

    @staticmethod
    def Process(instruction):
        Service.Call(instruction)
