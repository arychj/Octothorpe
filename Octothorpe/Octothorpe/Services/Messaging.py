import re, requests
from twilio.rest import TwilioRestClient

from Octothorpe.Log import Log
from Octothorpe.Service import Service

class Messaging(Service):

    def Send(self, protocol, to, message, subject = None, attachments = None):
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
            result = self._slack(to, message, attachments)
        else:
            result = {"error": f"Unkown protocol '{protocol}'"}

        if(result == None):
            result = {"success": "Message sent"}
        elif("error" in result):
            Log.Error(result["error"])

        return result

    def _email(self, to, message, subject):
        request_url = f"{self.Settings.GetString('email/base_url')}/{self.Settings.GetString('email/api_version')}/{self.Settings.GetString('email/domain')}/messages"
        request = requests.post(request_url, auth=("api", self.Settings.GetString("email/key")), data={
            "from": self.Settings.GetString("email/from"),
            "to": to,
            "subject": subject,
            "text": message
        })
    
    def _sms(self, to, message):
        client = TwilioRestClient(
            self.Settings.GetString("sms/username"),
            self.Settings.GetString("sms/password")
        )

        address = re.sub(self.Settings.GetString("sms/address_sanitize"), "", to)

        if len(address) == 10:
            address = '+1%s' % (address)
        elif len(toaddress) == 11:
            address = '+%s' % (address)
        else:
            return {"error": f"'{to}' is not a valid 10 or 11 digit number"}

        sms = client.sms.messages.create(
            to = address,
            from_ = self.Settings.GetString("sms/from"),
            body = message
        )
    
    def _phone(self, to, message):
        pass

    def _slack(self, to, message, attachments=None):
        from Octothorpe.Services.Slack.Slack import Slack

        if(Slack.IsValidAddress(to)):
            Slack.Send(to, message, attachments)
        else:
            return {"error": f"Invalid address '{to}'"}