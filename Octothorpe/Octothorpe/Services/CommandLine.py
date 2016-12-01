from ..Injector import Injector
from ..Manager import Manager
from ..Service import Service

class CommandLine(Service, Injector):
    def Start(self):
        self._running = True

        while(self._running):
            try:
                line = input()
                if(line in self.Settings.GetString("stop_signals").split(",")):
                    self.System("Stop signal received")
                    Manager.Stop()
                    break
                else:
                    result = self.Inject(line)
                    if(result != None):
                        print(result)
                    else:
                        print("Invalid instruction")
            except Exception as e:
                self.Error(e)

    def Stop(self):
        self._running = False
