import json

from .Database.Statement import Statement
from .Log import Log

class Rule:
    
    def __init__(self, id, producing_service, event_type, consuming_service, consuming_method, payload_transform):
        self.Id = id
        self.ProducingService = producing_service
        self.EventType = event_type
        self.ConsumingService = consuming_service
        self.ConsumingMethod = consuming_method
        self.PayloadTransform = payload_transform
        
    def PreparePayload(self, event):
        sPayload = "" + self.PayloadTransform

        for (k,v) in event.Payload.items():
            sPayload = sPayload.replace(f"|{k}|", v)

        return json.loads(sPayload)

    def Deactivate(self):
        statement = Statement.Get("Rules/Deactivate")
        statement.Execute({
            "id": self.Id
        })

    @staticmethod
    def GetMatches(event):
        rules = []

        statement = Statement.Get("Rules/Match")
        result = statement.Execute({
            "producing_service": event.Service,
            "event_type": event.Type
        })

        if(result.HasRows):
            for row in result.Rows:
                rules.append(Rule(
                    row["Id"],
                    event.Service,
                    event.Type,
                    row["ConsumingService"],
                    row["ConsumingMethod"],
                    row["PayloadTransform"]
                ))

        Log.Debug(f"Found {result.Count} matching rules for {event.Service}/{event.Type}")

        return rules

    @staticmethod
    def Create(producing_service, event_type, consuming_service, consuming_method, payload_transform):
        statment = Statement.Get("Rules/Create")
        result = statment.Execute({
            "producing_service": producing_service,
            "event_type": event_type,
            "consuming_service": consuming_service,
            "consuming_method": consuming_method,
            "payload_transform": payload_transform
        })

        return Rule(
            result.LastId,
            producing_service,
            event_type,
            consuming_service,
            consuming_method,
            payload_transform
        )

