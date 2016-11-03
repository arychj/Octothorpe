from Octothorpe.Service import Service

from random import randint
import time

class Test(Service):
    def Process(self, instruction):
        i = randint(0,5)
        time.sleep(i)
        print(f"{instruction.GetPriority()}| ({i}) {instruction.Payload}")

        self.Emit("emission", instruction, f">>> emitted instruction payload({instruction.Payload})")
        self.Emit("emission", instruction, ", ".join(self.Describe("Process")))
