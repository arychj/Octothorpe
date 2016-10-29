import glob, sqlite3

from .Config import Config

class Database:
    _connection = None

    @classmethod
    def GetConnection(cls):
        if(cls._connection == None):
            cls._connection = sqlite3.connect(Config.GetString("database/path"))

        return cls._connection

    @classmethod
    def CreateDatabase(cls):
        basepath = Config.GetString("database/queries/basepath")
        tables = glob.glob(f"{basepath}/Setup/CreateTable*.sql")

        for table in tables:
            name = table[table.rindex("/") + 1:-4]
            query = cls.GetNamedQuery(f"Setup/{name}")
            cls.GetConnection().execute(query)

        cls.GetConnection().commit()

    @classmethod
    def ExecuteNamedQuery(cls, name, parameters):
        query = cls.GetNamedQuery(name)

        cls.GetConnection().execute(query, parameters)
        cls.GetConnection().commit()

    @classmethod
    def GetNamedQuery(cls, name):
        basepath = Config.GetString("database/queries/basepath")
        name = name.replace(".", "",)
        data = None
        
        with open(f"{basepath}/{name}.sql", "r") as queryfile:
            data = queryfile.read()

        return data
