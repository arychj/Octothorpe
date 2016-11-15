import datetime, logging, os, sys, traceback

from .Config import Config

class Log:
    @classmethod
    def Debug(cls, message, tag=""):
        if(Config.GetBool("debug")):
            cls._console_write("debug", message, Color.Blue, tag)

    @classmethod
    def Entry(cls, message, tag=""):
        #temporary
        cls._console_write("entry", message, tag)
        return None
    
    @classmethod
    def System(cls, message, tag=""):
        #temporary
        cls._console_write("system", message, Color.Cyan, tag)
        return None

    @classmethod
    def Error(cls, message, tag=""):
        #log to db
        cls._console_write("error", message, Color.Yellow, tag)
        return None
    
    @classmethod
    def Exception(cls, e, tag=""):
        tb = e.__traceback__
        while(tb.tb_next != None):
            tb = tb.tb_next

        fname = os.path.split(tb.tb_frame.f_code.co_filename)[1]

        location = f"{fname}:{tb.tb_lineno}"
        type = f"[{e.__class__.__name__}]"
        message = str(e)

        cls._console_write("fatal", (f"{type:20}{location:20}{message}"), Color.Red, tag)

    @classmethod
    def _console_write(cls, type, message, color="", tag=""):
        type = f"[{type}]".upper()
        
        if(len(tag) > 0):
            tag = f"{Color.Magenta}[{tag}]{Color.Reset} "

        print(f"{color}{type:10}{Color.Reset} [{cls._get_timestamp()}]: {tag}{message}")

    @classmethod
    def _get_timestamp(cls):
        format = Config.GetString("logging/time_format");

        return datetime.datetime.now().strftime(format)

class Color:
    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'
    Magenta = '\033[95m'
    Cyan = '\033[96m'
    White = '\033[97m'
    Reset = '\033[0m'

