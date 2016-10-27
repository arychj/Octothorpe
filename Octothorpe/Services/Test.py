from Service import Service
from Event import Event

from random import randint
import time

class Test(Service):
    def Process(self, event):
        i = randint(0,5)
        time.sleep(i)
        print(f"({i}) {event.payload}")

        self.Emit(Event(1000 + 1, "Echo", ">>> emitted event payload"))
