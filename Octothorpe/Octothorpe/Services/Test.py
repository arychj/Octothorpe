from Octothorpe.Service import Service

from random import randint
import time

class Test(Service):
    @property
    def _emitted_event_types(self):
        return ["emission"]

    def Echo(self, **kwargs):
        s = ", ".join(["%s=%s" % (k, v) for (k, v) in kwargs.items()])
        self.Log(f"{self._instruction.ShortTag} > Echo: {s}")

        return kwargs

    def Test(self, text):
        i = randint(0,5)
        time.sleep(i)

        self.Log(f"{self._instruction.ShortTag} > Test: {text} [slept for {i}]")

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
