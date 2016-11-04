from Octothorpe.Service import Service

from random import randint
import time

class Test(Service):
    @property
    def _emitted_event_types(self):
        return ["emission"]

    def Echo(self, text):
        self.Log(f"{self._instruction.Id} ({self._instruction.GetPriority()}) > Echo: {text}")

    def Test(self, text):
        i = randint(0,5)
        time.sleep(i)

        self.Log(f"{self._instruction.Id} ({self._instruction.GetPriority()}) > Test: {text} [slept for {i}]")

        self.Emit("emission", {
        	"text": f">>> emitted instruction payload({text})"
        })

        self.Emit("emission", {
        	"text": ", ".join(self.Describe("MoreThanOneParamater"))
        })

    def MoreThanOneParamater(self, more, than, one, parameter):
        pass

    def RaiseException(self):
        raise Exception("I take umbrance to your call!!!")
