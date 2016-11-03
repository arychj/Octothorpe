#!/usr/bin/env python3
import sys, time

from Octothorpe.Config import Config
from Octothorpe.Database import Database
from Octothorpe.Instruction import Instruction
from Octothorpe.InstructionQueue import InstructionQueue
from Octothorpe.Log import Log
from Octothorpe.Manager import Manager

from random import randint

if len(sys.argv) != 2:
    print(f"\tUsage: {sys.argv[0]} config.xml")
else:
    Config.SetConfigFile(sys.argv[1])

#    Database.CreateDatabase()

    manager = Manager()
    manager.Start()

    InstructionQueue.Enqueue(Instruction(100, 1, time.time(), "Test", "RaiseException", None))

    for i in range(50):
        payload = "{\"text\":\"" + ("*" * i) + "\"}"
        instruction = Instruction(i, 1, time.time(), "Test", ("Echo" if randint(0,1) == 0 else "Test"), payload)
        InstructionQueue.Enqueue(instruction)

    while(1):
        try:
            line = input()
            if(line == "stop"):
                print("Stopping...")
                manager.Stop()
                break
            else:
                pieces = line.split(";")
                InstructionQueue.Enqueue(Instruction(0, 1, time.time(), pieces[0], pieces[1]))
        except Exception as e:
            Log.Exception(e)
