import re

from ..Shim import Shim

class SlackShim(Shim):

    def Outshimerate(self, instruction):
        result = None

        if(instruction.OutputTemplate != None and instruction.Result != None):
            result = instruction.OutputTemplate.format(**instruction.Result)
        else:
            result = instruction.Result

        return {"response": result}