import json

from .Config import Config
from .Database.Statement import Statement
from .Log import Log
from .Stipulation import Stipulation, StipulationType

class Rule:
    
    def __init__(self, id, producing_service, event_type, payload_stipulations, consuming_service, consuming_method, payload_transform):
        self.Id = id
        self.ProducingService = producing_service
        self.EventType = event_type
        self.Stipulations = payload_stipulations
        self.ConsumingService = consuming_service
        self.ConsumingMethod = consuming_method
        self.PayloadTransform = payload_transform

        self.Extras = {}

    def Match(self, event):
        if(event.Service != self.ProducingService):
            return False
        elif(event.Type != self.EventType):
            return False
        else:
            for stipulation in self.Stipulations:
                for (k, v) in event.Payload.items():
                    (passed, extras) = stipulation.Stipulate(k, v)
                    if(passed):
                        self.Extras.update(extras)
                    else:
                        return False

        return True

    def PreparePayload(self, event):
        sPayload = "" + self.PayloadTransform

        for (k, v) in {**event.Payload, **self.Extras}.items():
            sPayload = sPayload.replace(f"|{k}|", v)
        
        return json.loads(sPayload)

    def Deactivate(self):
        statement = Statement.Get("Rules/Deactivate")
        statement.Execute({
            "id": self.Id
        })

    @staticmethod
    def GetMatches(event):
        matches = []

        rules = Rule.GetRules(event.Service, event.Type)
        for rule in rules:
            if(rule.Match(event)):
                matches.append(rule)

        Log.Debug(f"Found {len(matches)} matching rules for {event.Service}/{event.Type}")

        return matches

    @staticmethod
    def GetRules(service, event):
        rules = Rule._get_rules_from_config(service, event)
        #rules.extend(Rule._get_rules_from_database(service, event))

        return rules

    @staticmethod
    def _get_rules_from_config(service, event):
        rules = []

        xRules = Config._raw(f"rules/rule[producing_service='{service}'][event_type='{event}']")
        for xRule in xRules:
            stipulations = []
            xStipulations = xRule.findall(f"stipulations/stipulation")
            for xStipulation in xStipulations:
                stipulations.append(Stipulation(
                    id = None,
                    type = StipulationType.Parse(xStipulation.find("type").text),
                    key = xStipulation.find("key").text,
                    stipulation = xStipulation.find("stipulation").text
                ))

            rules.append(Rule(
                id = None,
                producing_service = service,
                event_type = event, 
                payload_stipulations = stipulations,
                consuming_service = xRule.find("consuming_service").text, 
                consuming_method = xRule.find("consuming_method").text, 
                payload_transform = xRule.find("payload_transform").text, 
            ))

        return rules

    @staticmethod
    def _get_rules_from_database(service, event):
        rules = []

        statement = Statement.Get("Rules/Match")
        result = statement.Execute({
            "producing_service": service,
            "event_type": event
        })

        if(result.HasRows):
            for row in result.Rows:
                stipulations = []

                #get stipulations

                rules.append(Rule(
                    row["Id"],
                    service,
                    event,
                    stipulations,
                    row["ConsumingService"],
                    row["ConsumingMethod"],
                    row["PayloadTransform"]
                ))

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

