from Service import Service

class Echo(Service):
    def Process(self, event):
        print(event.payload)
