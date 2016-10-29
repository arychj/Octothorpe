import logging, os, sys, traceback

class Log:
    @classmethod
    def Debug(cls, message):
        return None

    @classmethod
    def Event(cls, message):
        return None
    
    @classmethod
    def Error(cls, message):
        return None
    
    @classmethod
    def Exception(cls, e):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        traceback.print_tb(exc_tb)

        location = f"{fname}:{exc_tb.tb_lineno}"
        type = f"[{exc_type.__name__}]"
        message = str(e)

        print(f"{location:20}{type:30}{message}")
