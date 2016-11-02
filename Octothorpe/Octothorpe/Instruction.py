
class Instruction(object):
    Id = None
    Service = None
    Payload = None

    def __init__(self, id, service, payload):
        self.Id = id
        self.Service = service
        self.Payload = payload

    def Complete(self):
        return None
