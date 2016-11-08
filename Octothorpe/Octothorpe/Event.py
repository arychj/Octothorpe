import json, time

from .Database.Statement import Statement

class Event:
    def __init__(self, id, instruction, service, type, payload, emitted_on):
        self.Id = id
        self.Instruction = instruction
        self.Service = service
        self.Type = type
        self.Payload = payload
        self.EmittedOn = emitted_on

        if(self.Id == None):
            self.CreateRecord()

    def CreateRecord(self):
        statement = Statement.Get("Events/Create")
        result = statement.Execute({
            "id_instruction": self.Instruction.Id,
            "service": self.Service,
            "type": self.Type,
            "payload": json.dumps(self.Payload),
            "emitted_on": Statement.FormatDatetime(self.EmittedOn)
        })

        self.Id = result.LastId

    @staticmethod
    def Create(instruction, service, type, payload):
        return Event(
            None,
            instruction,
            service,
            type,
            payload,
            time.time()
        )
