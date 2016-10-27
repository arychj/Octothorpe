import threading, time, queue

from Event import Event

from random import randint

class EventQueue:
    poll = True
    queue = queue.Queue(50)

    @classmethod
    def blah(cls):
        for i in range(50):
            payload = "*" * i
            event = Event(i, ("Echo" if randint(0,1) == 0 else "Test"), payload)
            cls.Push(event)
        
    @classmethod
    def HasEvents(cls):
        return (False if cls.queue.empty() else True)

    @classmethod
    def Push(cls, event):
        cls.queue.put(event, True)

    @classmethod
    def Next(cls):
        return cls.queue.get(True)

    @classmethod
    def StartPolling(cls):
        t = threading.Thread(target=cls.PollForEvents)
        t.start()
        
    @classmethod
    def PollForEvents(cls):
        while(cls.poll):
            x = 1
            time.sleep(1)
