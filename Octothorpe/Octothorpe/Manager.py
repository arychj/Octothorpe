import argparse
from random import randint

from .Config import Config
from .Injector import Injector
from .Instruction import Instruction
from .TaskQueue import TaskQueue
from .Log import Log
from .Service import Service
from .Setup import Setup

class Manager:

    @staticmethod
    def Start():
        parser = argparse.ArgumentParser()
        parser.add_argument("--config", dest ="config", required=True, help="Configuration File")
        parser.add_argument("--test", dest ="test", type=int, default=None, help="Generate and queue n test instructions")
        parser.add_argument("--setup", dest ="setup", action="store_true", help="Perform initial setup")

        args = parser.parse_args()
        Config.SetConfigFile(args.config)

        if(args.setup):
            Setup.Setup()

        if(args.test != None):
            for i in range(args.test):
                payload = "{\"text\":\"" + ("*" * i) + "\"}"
                instruction = Instruction.Create(
                    1,
                    "Test", 
                    ("Echo" if randint(0, 1) == 0 else "Test"), 
                    payload
                )

                TaskQueue.Enqueue(instruction)

        TaskQueue.Start()
        Injector.StartAll()

    @staticmethod
    def Stop():
        Log.System("Stopping system")

        TaskQueue.Stop()
        Injector.StopAll()
