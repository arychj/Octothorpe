import re

from ..Shim import Shim

class SlackShim(Shim):

    def Inbound(self, message):
        return self.CreateEvent(
            "message_received",
            {"message": message}
        )

    def Outbound(self, instruction):
        template = self.Settings.GetString(f"commands/command[@name='{self._command}']/response_template")
        result = template.format(instruction.Result)

        return result