
class Event:
    _id = None
    _instruction = None

    Service = None
    Type = None
    Payload = None

    def __init__(self, instruction, service, type, payload):
        self._instruction = instruction

        self.Service = service
        self.Type = type
        self.Payload = payload

        self.Log()

    def Log(self):
        #log event to database and get id

        self._id = 5000
