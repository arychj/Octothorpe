import json, time

from .Database.Statement import Statement
from .Log import Log
from .Rule import Rule
from .Task import Task, TaskType
from .TaskQueue import TaskQueue
from .Tools import Tools

#python circular dependency nonsense
import Octothorpe.Instruction

class Event(Task):

    @property
    def TaskType(self):
        return TaskType.Event

    @property
    def Priority(self):
        priority = 0
        priority += 50
        priority += -1 * (int(time.time()) - int(self.GivenOn))

        return priority

    def __init__(self, id, instruction, service, type, payload, emitted_on, processing_on = None, completed_on = None):
        super().__init__(
            given_on = emitted_on,
            processing_on = processing_on,
            completed_on = completed_on
        )

        self.Id = id
        self.Instruction = instruction
        self.Service = service
        self.Type = type
        self.Payload = payload
        self.EmittedOn = emitted_on

        self.OutputInstruction = None

        if(self.Id == None):
            self.CreateRecord()

    def Capture(self, service, method):
        self.CaptureService = service
        self.CaptureMethod = method

    def Process(self):
        rules = Rule.GetMatches(self)
        for rule in rules:
            instruction = Octothorpe.Instruction.Instruction.Create( #python circular dependency nonsense
                (1 if self.Instruction == None else self.Instruction.Level + 1), 
                rule.ConsumingService, 
                rule.ConsumingMethod, 
                rule.PreparePayload(self)
            )

            if(rule.OutputTemplate != None and rule.OutputTemplate.attrib['service'] == instruction.Service and rule.OutputTemplate.attrib['method'] == instruction.Method):
                instruction.OutputTemplate = rule.OutputTemplate.find("template").text
                self.OutputInstruction = instruction
                
            TaskQueue.Enqueue(instruction)

    def CreateRecord(self):
        statement = Statement.Get("Events/Create")
        result = statement.Execute({
            "id_instruction": (self.Instruction.Id if self.Instruction != None else None),
            "service": self.Service,
            "type": self.Type,
            "payload": json.dumps(self.Payload),
            "emitted_on": Tools.FormatDatetime(self.EmittedOn)
        })

        self.Id = result.LastId

    def Save(self):
        pass

    @staticmethod
    def Create(instruction, service, type, payload):
        event = Event(
            None,
            instruction,
            service,
            type,
            payload,
            time.time()
        )
        
        Log.Debug(f"Created event {event.Service}/{event.Type}:{event.Id}")

        return event
