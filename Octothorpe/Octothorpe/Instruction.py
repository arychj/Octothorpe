import sys, time

class Instruction(object):
    Id = None
    Level = None
    QueuedOn = None
    Service = None
    Payload = None

    def __init__(self, id, level, queued_on, service, payload):
        self.Id = id
        self.Level = level
        self.QueuedOn = queued_on
        self.Service = service
        self.Payload = payload

    def Complete(self):
        return None

    def GetPriority(self):
        priority = 0

        if(self.Id == -1):
            priority = sys.maxsize
        else:
            priority += self.Level * 10
            priority += int(time.time()) - int(self.QueuedOn)

        return priority

    def __lt__(self, other):
        return self.GetPriority() < other.GetPriority()

    @staticmethod
    def GetStopInstruction():
        return Instruction(-1, 0, 0, None, None)
