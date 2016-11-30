import glob

from .Config import Config
from .Database.Statement import Statement

class Setup:

    @staticmethod
    def Setup():
        Setup.SetupDatabase()

    @staticmethod
    def SetupDatabase():
        basepath = Config.GetString("database/queries/basepath")
        tables = glob.glob(f"{basepath}/Setup/*.sql")

        for table in tables:
            name = table[table.rindex("/") + 1:-4]
            statement = Statement.Get(f"Setup/{name}")
            statement.Execute()
