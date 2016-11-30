import sqlite3, threading, time

from ..Config import Config
from ..Log import Log

from .Result import Result
#from .Statement import Statement

class Database:
    _lock = threading.Lock()
    _cursor = None

    @classmethod
    def _shared_cursor(cls):
        if(cls._cursor == None):
            cls._connection = sqlite3.connect(Config.GetString("database/path"), check_same_thread=False)
            cls._connection.row_factory = sqlite3.Row
            cls._cursor = cls._connection.cursor()

            t = threading.Thread(
                target = cls._commit_changes,
                daemon = True
            )
            
            t.start()

        return cls._cursor

    #hokey, there's a better way of doing this
    @classmethod
    def Execute(cls, query, args = None, name = None):
        result = None

        cls._lock.acquire()
        try:
            if(args == None):
                cls._shared_cursor().execute(query)
            else:
                cls._shared_cursor().execute(query, args)

            if(query.strip().upper().startswith("SELECT")):
                rows = cls._shared_cursor().fetchall()
            else:
                rows = None

            result = Result(
                rows,
                cls._shared_cursor().lastrowid
            )
        except Exception as e:
            if(name == None):
                name = "unnamed"

            Log.Exception(e, f"Statement:{name}")
        finally:
            cls._lock.release()

        return result

    @classmethod
    def Finalize(cls):
        cls._shared_cursor().commit()
        cls._shared_cursor().connection._close()

    @classmethod
    def _commit_changes(cls):
        while(1):
            cls._lock.acquire()
            try:
                cls._shared_cursor().connection.commit()
            finally:
                cls._lock.release()

            time.sleep(1)
