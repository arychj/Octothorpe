from ..Injector import Injector
from ..Instruction import Instruction
from ..Manager import Manager

class CommandLineInjector(Injector):
    def Start(self):
        self._running = True

        while(self._running):
            try:
                line = input()
                if(line in self.GetString("stop_signals").split(",")):
                    self.Log("Stop signal received")
                    Manager.Stop()
                    break
                else:
                    instruction = Instruction.Parse(line)
                    response = self.Inject(instruction=instruction)
            except Exception as e:
                self.Error(e)

    def Stop(self):
        self._running = False
