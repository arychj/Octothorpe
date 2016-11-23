import os, time, re
from functools import lru_cache
from .slackclient import SlackClient

from ...Injector import Injector

class SlackInjector(Injector):
    _client = None

    @property
    @staticmethod
    def Client():
        return SlackInjector._client

    def Connect(self):
        SlackInjector.Client = SlackClient(self.GetString("api_key"))
        return SlackInjector.Client.rtm_connect()

    def Handle(self, channel, user, message):
        self.Debug(f"Received message from {SlackInjector._resolve_channel_id(channel, user)} ({channel}): {message[:25]}")

        match = None
        commands = self.GetMultiple("commands/command")
        for command in commands:
            match = re.match(command.find("pattern").text, message, re.IGNORECASE)
            if(match != None):
                break

        if(match != None):
            self.Debug(f"Matched to command '{command.attrib['name']}'")

            response = self.Inject(
                command.find("service").text,
                command.find("method").text,
                match.groupdict()
            )

            SlackInjector.Send(channel, response)

    def ParsePayload(self, payload):
        if payload and len(payload) > 0:
            for output in payload:
                if output and 'text' in output and 'bot_id' not in output:
                    return output['channel'], output['user'], output['text']

        return None, None, None

    def Start(self):
        read_interval = self.GetInt("read_interval")
        self._running = True

        if self.Connect():
            self.Log("Connection established")

            while self._running:
                channel, user, message = self.ParsePayload(self.Client.rtm_read())
                if message and channel:
                    self.Handle(channel, user, message)

                time.sleep(read_interval)
        else:
            self.Log("Connection failed")

    def Stop(self):
        self._running = False

    @classmethod
    def IsValidAddress(cls, address):
        return (address and (address[0] == "#" or address == "@"))
            
    @classmethod
    def Send(cls, channel_name, message):
        cls.Client.api_call("chat.postMessage", channel=channel_name, text=message, as_user=True)
    
    @classmethod
    @lru_cache(maxsize=8)
    def _resolve_channel_id(cls, id, user):
        name = None

        if(id[0] == "D"):
            response = cls.Client.api_call("users.info", user=user, as_user=True)
            name = f"@{response['user']['name']}"
        else:
            response = cls.Client.api_call("channels.list", as_user=True)
            channel = list(filter(lambda c: c["id"] == id, response["channels"]))[0]
            name = f"#{channel['name']}"

        return name