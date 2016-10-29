from Octothorpe.Service import Service

class Echo(Service):
    def Process(self, instruction):
        print(instruction.Payload)
