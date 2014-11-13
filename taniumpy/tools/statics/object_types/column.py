

class Column(object):

    def __init__(self):
        self.what_hash = None
        self.display_name = None
        self.result_type = None

    @classmethod
    def fromSOAPElement(cls, el):
        result = Column()
        val = el.find('wh')
        if val is not None:
            result.what_hash = int(val.text)
        val = el.find('dn')
        if val is not None:
            result.display_name = val.text
        val = el.find('rt')
        if val is not None:
            result.result_type = int(val.text)
        return result
