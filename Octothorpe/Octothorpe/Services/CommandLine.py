from ..Injector import Injector
from ..Instruction import Instruction
from ..TaskQueue import TaskQueue
from ..Manager import Manager
from ..Service import Service

class CommandLine(Service, Injector):

    @property
    def _emitted_event_types(self):
        return ["instruction"]

    def _injector_start(self):
        self._running = True

        while(self._running):
            try:
                line = input()
                if(line in self.Settings.GetString("stop_signals").split(",")):
                    self.System("Stop signal received")
                    Manager.Stop()
                    break
                else:
                    instruction = Instruction.Parse(line)
                    TaskQueue.Enqueue(instruction)
                    instruction.WaitUntilComplete()

                    if(instruction.Result != None):
                        print(instruction.Result)
                    else:
                        print("Invalid instruction")
            except Exception as e:
                self.Error(e)

    def _injector_stop(self):
        self._running = False
