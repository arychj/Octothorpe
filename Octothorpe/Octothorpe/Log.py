import datetime, logging, os, sys, traceback

from .Config import Config

class Log:
    @classmethod
    def Debug(cls, message):
        if(Config.GetBool("debug")):
            cls._console_write("debug", message, Color.Blue)

    @classmethod
    def Entry(cls, message):
        #temporary
        cls._console_write("event", message)
        return None
    
    @classmethod
    def Error(cls, message):
        #Color.Yellow
        return None
    
    @classmethod
    def Exception(cls, e):
        tb = e.__traceback__
        while(tb.tb_next != None):
            tb = tb.tb_next

        fname = os.path.split(tb.tb_frame.f_code.co_filename)[1]

        location = f"{fname}:{tb.tb_lineno}"
        type = f"[{e.__class__.__name__}]"
        message = str(e)

        cls._console_write("fatal", (f"{type:20}{location:20}{message}"), Color.Red)

    @classmethod
    def _console_write(cls, type, message, color = ""):
        type = f"[{type}]".upper()
        print(f"{color}{type:10}{Color.Reset} [{cls._get_timestamp()}]: {message}")

    @classmethod
    def _get_timestamp(cls):
        format = Config.GetString("logging/time_format");

        return datetime.datetime.now().strftime(format)

class Color:
    Blue = '\033[94m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Red = '\033[91m'
    Reset = '\033[0m'

