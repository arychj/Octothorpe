#!/usr/bin/env python3
import argparse, sys

from Octothorpe.Config import Config
from Octothorpe.Database.Database import Database
from Octothorpe.Instruction import Instruction
from Octothorpe.Log import Log
from Octothorpe.Manager import Manager

from random import randint

parser = argparse.ArgumentParser()
parser.add_argument("--config", dest ="config", required=True, help="Configuration File")
parser.add_argument("--test", dest ="test", type=int, default=None, help="Generate and queue n test instructions")
parser.add_argument("--setup", dest ="setup", action="store_true", help="Perform initial setup")

args = parser.parse_args()
Config.SetConfigFile(args.config)

if(args.setup):
    Database.Setup()

if(args.test != None):
    for i in range(args.test):
        payload = "{\"text\":\"" + ("*" * i) + "\"}"
        instruction = Instruction.Create(
            1,
            "Test", 
            ("Echo" if randint(0,1) == 0 else "Test"), 
            payload
        )

        Manager.Queue(instruction)

Manager.Start()