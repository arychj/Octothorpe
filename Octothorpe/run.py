#!/usr/bin/env python3
import sys

from Octothorpe.Config import Config
from Octothorpe.Database import Database
from Octothorpe.Manager import Manager

if len(sys.argv) != 2:
    print(f"\tUsage: {sys.argv[0]} config.xml")
else:
    Config.SetConfigFile(sys.argv[1])

#    Database.CreateDatabase()

    manager = Manager()
    manager.Start()
