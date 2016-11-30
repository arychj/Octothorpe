from ..Config import Config
from ..Log import Log

from .Database import Database

class Statement:

    def __init__(self, name, statement):
        self._name = name
        self._statement = statement

    def Execute(self, args = None):
        return Database.Execute(self._statement, args, self._name)

    @classmethod
    def Get(cls, name):
        basepath = Config.GetString("database/queries/basepath")
        name = name.replace(".", "")
        
        sStatement = None
        with open(f"{basepath}/{name}.sql", "r") as statement_file:
            sStatement = statement_file.read()

        if(sStatement == None):
            return None
        else:
            return Statement(name, sStatement)
