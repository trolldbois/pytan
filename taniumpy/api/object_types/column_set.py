from .column import Column

class ColumnSet(object):

    def __init__(self):
        self.columns = []

    @classmethod
    def fromSOAPElement(cls, el):
        result = ColumnSet()
        columns = el.findall('./c')
        for column in columns:
            result.columns.append(Column.fromSOAPElement(column))
        return result