#!/usr/bin/env python3
import sys

from Octothorpe.Config import Config
from Octothorpe.Database import Database
from Octothorpe.Instruction import Instruction
from Octothorpe.InstructionQueue import InstructionQueue
from Octothorpe.Manager import Manager

if len(sys.argv) != 2:
    print(f"\tUsage: {sys.argv[0]} config.xml")
else:
    Config.SetConfigFile(sys.argv[1])

#    Database.CreateDatabase()

    manager = Manager()
    manager.Start()

    while(1):
        line = input()
        if(line == "stop"):
            manager.Stop()
            break
        else:
            pieces = line.split(";")
            InstructionQueue.Push(Instruction(0, pieces[0], pieces[1]))
