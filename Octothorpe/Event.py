
class Event:
    def __init__(self, id, service, payload):
        self.id = id
        self.service = service
        self.payload = payload

    def Complete(self):
        return None
