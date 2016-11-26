import json, re, sys, time, threading, uuid

from .Config import Config
from .Database.Statement import Statement
from .Log import Log

class Instruction(object):
    
    def __init__(self, id, ident, level, service, method, payload, given_on, processing_on = None, completed_on = None):
        self.Id = id
        self.Ident = ident
        self.Level = level
        self.Service = service
        self.Method = method
        self.Payload = Instruction._parse_payload(payload)
        self.Result = None
        self.GivenOn = given_on
        self.ProcessingOn = processing_on
        self.CompletedOn = completed_on

        self._lock = threading.Lock()
        if(self.CompletedOn == None):
            self._lock.acquire()

        if(self.Id == None):
            self.CreateRecord()

    @property
    def Priority(self):
        priority = 0
        priority += self.Level * 10
        priority += -1 * (int(time.time()) - int(self.GivenOn))

        return priority

    @property
    def ShortIdent(self):
        if(self.Ident == None):
            return None
        else:
            return self.Ident[:8]

    @property
    def Tag(self):
        if(self.Id == None or self.Ident == None):
            return None
        else:
            return f"{self.Ident}:{self.Id}/{self.Priority}/{self.Level}/{self.Service}.{self.Method}"

    @property
    def ShortTag(self):
        if(self.Id == None or self.Ident == None):
            return None
        else:
            return f"{self.ShortIdent}:{self.Id}/{self.Level}/{self.Priority}"

    @property
    def ProcessingTime(self):
        if(self.ProcessingOn == None or self.CompletedOn == None):
            return None
        else:
            return self.CompletedOn - self.ProcessingOn

    @property
    def WaitingTime(self):
        if(self.GivenOn == None or self.ProcessingOn == None):
            return None
        else:
            return self.ProcessingOn - self.GivenOn

    @property
    def IsComplete(self):
        return (self.CompletedOn != None)

    def CreateRecord(self):
        self.Ident = Instruction._generate_ident()

        statement = Statement.Get("Instructions/Create")
        result = statement.Execute({
            "ident": self.Ident,
            "level": self.Level,
            "service": self.Service,
            "method": self.Method,
            "payload": json.dumps(self.Payload),
            "given_on": Statement.FormatDatetime(self.GivenOn)
        })

        self.Id = result.LastId

    def Processing(self):
        self.ProcessingOn = time.time()

    def Complete(self):
        if(self.Id != None):
            self.CompletedOn = time.time()

            statement = Statement.Get("Instructions/Complete")
            statement.Execute({
                "id": self.Id,
                "processing_on": Statement.FormatDatetime(self.ProcessingOn),
                "completed_on": Statement.FormatDatetime(self.CompletedOn)
            })

            self._lock.release()
        else:
            raise Exception("Cannot complete unsaved instruction.")

    def WaitUntilComplete(self):
        if(self._lock.locked()):
            self._lock.acquire()
            self._lock.release()

    def Fail(self):
        self.Complete()

    def __lt__(self, other):
        if(self.Id == -1):
            return True
        elif(other.Id == -1):
            return False
        else:
            sp = self.Priority
            op = other.Priority

            if(sp == op):
                return self.GivenOn < other.GivenOn
            else:
                return  sp < op

    @staticmethod
    def Create(level, service, method, payload):
        instruction = Instruction(
            None,
            None,
            level,
            service,
            method,
            payload,
            time.time()
        )

        Log.Debug(f"Created instruction {instruction.ShortTag}")

        return instruction

    @staticmethod
    def Load():
        pass

    @staticmethod
    def GetStopInstruction():
        return Instruction(-1, 0, 0, None, None, None, None)

    @staticmethod
    def Parse(s):
        instruction = None

        m = re.match("^(?P<Service>.*?)\.(?P<Method>.*?)\((?P<Payload>.*)\)$", s)
        if(m != None):
            instruction = Instruction.Create(
                1,
                m.group("Service"),
                m.group("Method"),
                Instruction._parse_payload(m.group("Payload"))
            )
        
        return instruction 

    @staticmethod
    def _parse_payload(s):
        if((s == None) or (len(s) == 0)):
            return None
        elif(isinstance(s, str)):
            Log.Debug(f"Decoding JSON payload: {s}")
            return json.loads(s)
        elif(isinstance(s, dict)):
            return s
        else:
            raise Exception("Invalid payload format")

    @staticmethod
    def _generate_ident():
        ident = uuid.uuid4()
        return ident.hex
