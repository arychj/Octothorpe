import json

from .Database.Statement import Statement

class Rule:
    
    def __init__(self, id, event_type, service, method, payload_transform):
        self.Id = id
        self.EventType = event_type
        self.Service = service
        self.Method = method
        self.PayloadTransform = payload_transform
        
    def PreparePayload(self, event):
        sPayload = "" + self.PayloadTransform

        for (k,v) in event.Payload.items():
            sPayload = sPayload.replace(f"|{k}|", v)

        return json.loads(sPayload)

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
                    event.Type,
                    row["ConsumingService"],
                    row["ConsumingMethod"],
                    row["PayloadTransform"]
                ))

        return rules

