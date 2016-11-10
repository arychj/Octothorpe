import sys, threading

from .Injector import Injector
from .InstructionQueue import InstructionQueue
from .Service import Service

class Manager:

    @staticmethod
    def Start():
        Service._queue = InstructionQueue

        InstructionQueue.Start()
        Injector.StartAll()

    @staticmethod
    def Stop():
        InstructionQueue.Stop()
        Injector.StopAll()

    @staticmethod
    def Queue(instruction):
        InstructionQueue.Enqueue(instruction)

    @staticmethod
    def Process(instruction):
        Service.Call(instruction)

