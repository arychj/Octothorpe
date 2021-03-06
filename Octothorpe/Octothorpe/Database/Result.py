
class Result:
    def __init__(self, rows, last_id):
        self.Rows = rows
        self.LastId = last_id

    @property
    def HasRows(self):
        return ((self.Rows != None) and (len(self.Rows) > 0))

    @property
    def Count(self):
        return (0 if self.Rows == None else len(self.Rows))
