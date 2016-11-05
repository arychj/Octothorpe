import datetime, sqlite3, threading

from .Result import Result
from ..Config import Config
from ..Log import Log

class Statement:
    _lock = threading.Lock()
    _cursor = None

    def __init__(self, statement):
        self._statement = statement

    @classmethod
    def _shared_cursor(cls):
        if(cls._cursor == None):
            cls._connection = sqlite3.connect(Config.GetString("database/path"), check_same_thread=False)
            cls._cursor = cls._connection.cursor()

        return cls._cursor

    #hokey, there's a better way of doing this
    def Execute(self, args = None):
        result = None

        self._lock.acquire()
        try:
            if(args == None):
                self._shared_cursor().execute(self._statement)
            else:
                self._shared_cursor().execute(self._statement, args)

            if(self._statement.strip().upper().startswith("SELECT")):
                rows = self._shared_cursor().fetchall()
            else:
                rows = None

            result = Result(
                rows,
                self._shared_cursor().lastrowid
            )

            self._shared_cursor().connection.commit()
        except Exception as e:
            Log.Exception(e)
        finally:
            self._lock.release()

        return result

    @classmethod
    def Get(cls, name):
        basepath = Config.GetString("database/queries/basepath")
        name = name.replace(".", "",)
        
        sStatement = None
        with open(f"{basepath}/{name}.sql", "r") as statement_file:
            sStatement = statement_file.read()

        if(sStatement == None):
            return None
        else:
            return Statement(sStatement)

    @classmethod
    def Finalize(cls):
        cls._shared_cursor().commit()
        cls._shared_cursor().connection._close()

    @staticmethod
    def FormatDatetime(d):
        return datetime.datetime.fromtimestamp(d).strftime(
            Config.GetString("logging/time_format")
        )

