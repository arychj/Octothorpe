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
parser.add_argument("--test", dest ="test", action="store_true", help="Generate and queue test instructions")
parser.add_argument("--setup", dest ="setup", action="store_true", help="Perform initial setup")

args = parser.parse_args()
Config.SetConfigFile(args.config)

if(args.setup):
    Database.Setup()

if(args.test):
    for i in range(50):
        payload = "{\"text\":\"" + ("*" * i) + "\"}"
        instruction = Instruction.Create(
            1,
            "Test", 
            ("Echo" if randint(0,1) == 0 else "Test"), 
            payload
        )

        Manager.Queue(instruction)

Manager.Start()

while(1):
    try:
        line = input()
        if(line == "stop"):
            print("Stopping...")
            Manager.Stop()
            break
        else:
            instruction = Instruction.Parse(line)
            Manager.Queue(instruction)
    except Exception as e:
        Log.Exception(e)
