import time

from Config import Config
from EventQueue import EventQueue
from Log import Log
from Worker import Worker

class Manager:
    def Start(self):
        EventQueue.blah()
        EventQueue.StartPolling()
        self.Loop()

    def Loop(self):
        while(True):
            event = EventQueue.Next()
            try:
                while((event != None) and Worker.IsAvailable()):
                    Worker.Process(event)
                    event = EventQueue.Next()
            except Exception as e:
                Log.Exception(e)

