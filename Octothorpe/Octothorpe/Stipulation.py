import re
from enum import Enum

class Stipulation:
    
    def __init__(self, id, type, key, stipulation):
        self.Id = id
        self.Type = type
        self.Key = key
        self.Stipulation = stipulation

    def Stipulate(self, key, value):
        passed = True
        extras = {}

        if(key == self.Key):
            if(self.Type == StipulationType.Regex):
                match = re.match(self.Stipulation, value)
                if(match != None):
                    extras = match.groupdict()
                else:
                    passed = False
            elif(self.Type == StipulationType.Equals):
                passed = (value == self.Stipulation)
            elif(self.Type == StipulationType.LessThan):
                passed = (value <= self.Stipulation)
            elif(self.Type == StipulationType.GreaterThan):
                passed = (value >= (self.Stipulation))
            elif(self.Type == StipulationType.Contains):
                passed = value.contains(self.Stipulation)
            elif(self.Type == StipulationType.StartsWith):
                passed = value.startswith(self.Stipulation)
            elif(self.Type == StipulationType.EndsWith):
                passed = value.endswith(self.Stipulation)

        return (passed, extras)

class StipulationType(Enum):
    Regex = 0
    Equals = 1
    LessThan = 2
    GreaterThan = 3
    Contains = 4
    StartsWith = 5
    EndsWith = 6

    @staticmethod
    def Parse(s):
        return getattr(StipulationType, s)