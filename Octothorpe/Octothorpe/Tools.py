import datetime

from .Config import Config

class Tools:

    @staticmethod
    def FormatDatetime(d):
        return datetime.datetime.fromtimestamp(d).strftime(
            Config.GetString("logging/time_format")
        )
        