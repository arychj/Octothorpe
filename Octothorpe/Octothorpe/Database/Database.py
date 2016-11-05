import glob

from ..Config import Config
from .Statement import Statement

class Database:

    @classmethod
    def Setup(cls):
        basepath = Config.GetString("database/queries/basepath")
        tables = glob.glob(f"{basepath}/Setup/*.sql")

        for table in tables:
            name = table[table.rindex("/") + 1:-4]
            statement = Statement.Get(f"Setup/{name}")
            statement.Execute()

