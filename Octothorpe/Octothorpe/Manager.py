import sys, threading

from .Injector import Injector
from .TaskQueue import TaskQueue
from .Log import Log
from .Service import Service
from .Event import Event

class Manager:

    @staticmethod
    def Start():
        TaskQueue.Start()
        Injector.StartAll()

    @staticmethod
    def Stop():
        Log.System("Stopping system")

        TaskQueue.Stop()
        Injector.StopAll()

    @staticmethod
    def Queue(instruction):
        TaskQueue.Enqueue(instruction)

    @staticmethod
    def Process(instruction):
        Service.Call(instruction)
