from Octothorpe.Service import Service

from random import randint
import time

class Test(Service):
    def Echo(self, instruction):
        print(f"{instruction.Id} ({instruction.GetPriority()}): Echo: {instruction.Payload}")

    def Test(self, instruction):
        i = randint(0,5)
        time.sleep(i)
        print(f"{instruction.Id} ({instruction.GetPriority()}): Test: {instruction.Payload} [slept for {i}]")

        self.Emit("emission", instruction, f">>> emitted instruction payload({instruction.Payload})")
        self.Emit("emission", instruction, ", ".join(self.Describe("Process")))
