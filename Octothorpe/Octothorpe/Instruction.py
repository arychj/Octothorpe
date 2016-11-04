import json, re, sys, time

from .Log import Log

class Instruction(object):
    Id = None
    Level = None
    QueuedOn = None
    Service = None
    Method = None
    Payload = None

    def __init__(self, id, level, queued_on, service, method, payload):
        self.Id = id
        self.Level = level
        self.QueuedOn = queued_on
        self.Service = service
        self.Method = method
        self.Payload = Instruction._parse_payload(payload)    

    def Record(self):
        self.Id = 6000

        return None

    def Complete(self):
        return None

    def GetPriority(self):
        priority = 0
        priority += self.Level * 10
        priority += -1 * (int(time.time()) - int(self.QueuedOn))

        return priority

    def __lt__(self, other):
        if(self.Id == -1):
            return True
        elif(other.Id == -1):
            return False
        else:
            sp = self.GetPriority()
            op = other.GetPriority()

            if(sp == op):
                return self.QueuedOn < other.QueuedOn
            else:
                return  sp < op

    @staticmethod
    def GetStopInstruction():
        return Instruction(-1, 0, 0, None, None, None)

    @staticmethod
    def Parse(s):
        instruction = None

        m = re.match("^(?P<Service>.*?)\.(?P<Method>.*?)\((?P<Payload>.*)\)$", s)
        if(m != None):
            instruction = Instruction(
                0,
                1,
                time.time(),
                m.group("Service"),
                m.group("Method"),
                Instruction._parse_payload(m.group("Payload"))
            )
        
        return instruction 

    @staticmethod
    def _parse_payload(s):
        if(s == None):
            return None
        elif(isinstance(s, str)):
            Log.Debug(f"Decoding JSON payload: {s}")
            return json.loads(s)
        elif(isinstance(s, dict)):
            return s
        else:
            raise Exception("Invalid payload format")
