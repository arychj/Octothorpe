from Octothorpe.Service import Service

from random import randint
import time

from Octothorpe.Injectors.Slack.SlackInjector import SlackInjector

class Test(Service):
    _random_sleep_count = 0

    @property
    def _emitted_event_types(self):
        return ["emission"]

    def Print(self, words):
        self.Log(f"{self._instruction.Tag} > Print: {words}")

    def Echo(self, **kwargs):
        s = ", ".join(["%s=%s" % (k, v) for (k, v) in kwargs.items()])
        self.Log(f"{self._instruction.Tag} > Echo: {s}")

        return kwargs

    def Test(self, text):
        i = randint(0,5)
#        time.sleep(i)

        self.Log(f"{self._instruction.Tag} > Test: {text} [slept for {i}]")

        self.Emit("emission", {
        	"text": f">>> emitted instruction payload({text})"
        })

        self.Emit("emission", {
        	"text": ", ".join(self.Describe("MoreThanOneParamater"))
        })

    def MoreThanOneParamater(self, more, than, one, parameter):
        pass

    def RandomSleep(self):
        seq = Test._random_sleep_count
        Test._random_sleep_count=Test._random_sleep_count+1

        i = randint(0,5)
        time.sleep(i)

        return {"seq": seq, "seconds": i}

    def RaiseException(self):
        raise Exception("I take umbrance to your call!!!")

    def Slack(self, to, message):
        if(SlackInjector.IsValidAddress(to)):
            SlackInjector.Send(to, message)
        else:
            Log.Error(f"Invalid address '{to}'")
