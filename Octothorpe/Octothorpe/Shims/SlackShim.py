import re

from ..Shim import Shim

class SlackShim(Shim):

    def Inbound(self, message):
        instruction = None

        match = None
        commands = self.GetMultiple("commands/command")
        for command in commands:
            match = re.match(command.find("pattern").text, message, re.IGNORECASE)
            if(match != None):
                self.Debug(f"Matched to command '{command.attrib['name']}'")

                self._command = command.attrib['name']

                xParameters = self.GetMultiple(f"commands/command[@name='{self._command}']/parameters/parameter")

                parameters = {}
                for xParameter in xParameters:
                    parameters[xParameter.attrib["name"]] = xParameter.text

                instruction = SlackShim.CreateInstruction(
                    command.find("service").text,
                    command.find("method").text,
                    {**parameters, **match.groupdict()}
                )

                break
        
        return instruction

    def Outbound(self, instruction):
        template = self.GetString(f"commands/command[@name='{self._command}']/response_template")
        result = template.format(instruction.Result)

        return result