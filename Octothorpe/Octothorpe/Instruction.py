import json, re, sys, time 

from .Config import Config
from .Database.Statement import Statement
from .Log import Log
from .Service import Service
from .Task import Task, TaskType
from .Tools import Tools

class Instruction(Task):
    
    @property
    def TaskType(self):
        return TaskType.Instruction

    @property
    def Priority(self):
        priority = 0
        priority += self.Level * 10
        priority += -1 * (int(time.time()) - int(self.GivenOn))

        return priority

    @property
    def FullTag(self):
        if(self.Id == None or self.Ident == None):
            return None
        else:
            return f"{self.Ident}:{self.Id}/{self.Level}/{self.Priority}/{self.Service}.{self.Method}"

    @property
    def Tag(self):
        if(self.Id == None or self.Ident == None):
            return None
        else:
            return f"{self.ShortIdent}:{self.Id}/{self.Level}/{self.Priority}"

    def __init__(self, id, ident, level, service, method, payload, given_on, processing_on = None, completed_on = None):
        super().__init__(
            given_on = given_on,
            processing_on = processing_on,
            completed_on = completed_on,
            ident = ident
        )

        self.Id = id
        self.Level = level
        self.Service = service
        self.Method = method
        self.Payload = Instruction._parse_payload(payload)
        self.Result = None

        self.OutputTemplate = None

        if(self.Id == None):
            self.CreateRecord()

    def CreateRecord(self):
        statement = Statement.Get("Instructions/Create")
        result = statement.Execute({
            "ident": self.Ident,
            "level": self.Level,
            "service": self.Service,
            "method": self.Method,
            "payload": json.dumps(self.Payload),
            "given_on": Tools.FormatDatetime(self.GivenOn)
        })

        self.Id = result.LastId

    def Process(self):
        Service.Process(self)

    def Save(self):
        if(self.Id != None):
            statement = Statement.Get("Instructions/Complete")
            statement.Execute({
                "id": self.Id,
                "processing_on": Tools.FormatDatetime(self.ProcessingOn),
                "completed_on": Tools.FormatDatetime(self.CompletedOn)
            })
        else:
            raise Exception("Cannot complete unsaved instruction.")

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

        Log.Debug(f"Created instruction {instruction.Tag}")

        return instruction

    @staticmethod
    def Load():
        pass

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

