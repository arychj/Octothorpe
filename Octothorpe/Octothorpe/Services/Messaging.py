import re
from twilio.rest import TwilioRestClient

from Octothorpe.Log import Log
from Octothorpe.Service import Service

class Messaging(Service):

    def Send(self, protocol, to, message, subject = None):
        Log.Debug(f"Sending message to {protocol}/{to}")

        result = None

        protocol = protocol.lower()
        if(protocol == "email"):
            result = self._email(to, message, subject)
        elif(protocol == "sms"):
            result = self._sms(to, message)
        elif(protocol == "phone"):
            result = self._phone(to, message)
        elif(protocol == "slack"):
            result = self._slack(to, message)
        else:
            result = {"error": f"Unkown protocol '{protocol}'"}

        if(result == None):
            result = {"success": "Message sent"}
        elif("error" in result):
            Log.Error(result["error"])

        return result

    def _email(self, to, message, subject):
        pass
    
    def _sms(self, to, message):
        client = TwilioRestClient(
            self.GetString("sms/username"),
            self.GetString("sms/password")
        )

        address = re.sub(self.GetString("sms/address_sanitize"), "", to)

        if len(address) == 10:
            address = '+1%s' % (address)
        elif len(toaddress) == 11:
            address = '+%s' % (address)
        else:
            return {"error": f"'{to}' is not a valid 10 or 11 digit number"}

        sms = client.sms.messages.create(
            to = address,
            from_ = self.GetString("sms/from"),
            body = message
        )
    
    def _phone(self, to, message):
        pass

    def _slack(self, to, message):
        from Octothorpe.Injectors.Slack.SlackInjector import SlackInjector

        if(SlackInjector.IsValidAddress(to)):
            SlackInjector.Send(to, message)
        else:
            return {"error": f"Invalid address '{to}'"}